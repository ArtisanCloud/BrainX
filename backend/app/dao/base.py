from datetime import datetime

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta, Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Any, TypeVar, Generic, Optional, Type, Tuple, Union, Sequence

# 定义 ModelType 类型变量，限定为 SQLAlchemy 的 DeclarativeMeta
ModelType = TypeVar('ModelType', bound=DeclarativeMeta)


class BaseDAO(Generic[ModelType]):
    def __init__(self, db: Union[AsyncSession, Session], model: Type[ModelType]):
        self.db = db
        self.model = model

    async def async_create(self, obj: ModelType) -> Tuple[
        Optional[ModelType], Optional[SQLAlchemyError]]:
        """
        创建新的模型对象
        """
        if isinstance(self.db, AsyncSession):
            # print(obj)
            try:
                self.db.add(obj)
                await self.db.flush()
                await self.db.refresh(obj)  # 刷新对象以获取数据库中的最新状态

                return obj, None
            except SQLAlchemyError as e:
                return None, e
        else:
            raise TypeError("a_create method requires an AsyncSession")

    def sync_create(self, obj: ModelType) -> Tuple[
        Optional[ModelType], Optional[SQLAlchemyError]]:
        """
        创建新的模型对象
        """
        if isinstance(self.db, Session):
            # print(obj)
            try:
                self.db.add(obj)
                self.db.flush()
                self.db.refresh(obj)  # 刷新对象以获取数据库中的最新状态

                return obj, None
            except SQLAlchemyError as e:
                return None, e
        else:
            raise TypeError("sync_create method requires an Session")

    async def async_create_many(self, objs: List[ModelType]) -> Tuple[
        Optional[List[ModelType]], Optional[SQLAlchemyError]]:
        """
        创建新的模型对象
        """
        if isinstance(self.db, AsyncSession):
            try:
                self.db.add_all(objs)
                await self.db.flush()
                # print(objs)
                return objs, None
            except SQLAlchemyError as e:

                return None, e
        else:
            raise TypeError("async_create_many method requires an AsyncSession")

    def sync_create_many(self, objs: List[ModelType]) -> Tuple[
        Optional[List[ModelType]], Optional[SQLAlchemyError]]:
        """
        创建新的模型对象
        """
        if isinstance(self.db, Session):
            try:
                self.db.add_all(objs)
                self.db.flush()
                # print(objs)
                return objs, None
            except SQLAlchemyError as e:

                return None, e
        else:
            raise Exception("sync_create_many method requires an Session")

    async def async_get_by_uuid(self, uuid: str) -> Tuple[Optional[ModelType], Optional[SQLAlchemyError]]:
        """
        根据 UUID 获取模型对象
        """
        if isinstance(self.db, AsyncSession):
            try:
                result = await self.db.execute(select(self.model).filter(self.model.uuid == uuid))
                return result.scalar_one_or_none(), None
            except SQLAlchemyError as e:
                return None, e
        else:
            raise Exception("async_get_by_uuid method requires an AsyncSession")

    async def sync_get_by_uuid(self, uuid: str) -> Tuple[Optional[ModelType], Optional[SQLAlchemyError]]:
        """
        根据 UUID 获取模型对象
        """
        if isinstance(self.db, Session):
            try:
                result = self.db.execute(select(self.model).filter(self.model.uuid == uuid))
                return result.scalar_one_or_none(), None
            except SQLAlchemyError as e:
                return None, e
        else:
            raise Exception("sync_get_by_uuid method requires an Session")

    async def async_get_objects_by_conditions(self, conditions: Dict[str, Any]) -> Tuple[
        Optional[Sequence[ModelType]], Optional[SQLAlchemyError]]:
        """
        根据给定的条件查询模型对象
        """
        try:
            query = select(self.model)
            filters = self._build_filters(conditions)

            if filters:
                query = query.filter(and_(*filters))

            # 打印生成的 SQL 查询语句
            # query_str = str(query)
            # print(conditions)
            # print(f"Generated SQL query: {query_str}")

            result = await self.db.execute(query)
            objects = result.scalars().all()
            return objects, None
        except SQLAlchemyError as e:
            return None, e
        except ValueError as ve:
            return None, ve

    def _build_filters(self, conditions: Dict[str, Any]) -> List:
        """
        构建查询过滤器列表
        """
        filters = []
        for field, value in conditions.items():
            if isinstance(value, dict):
                if 'in' in value:
                    filters.append(getattr(self.model, field).in_(value['in']))
                elif '!=' in value:
                    filters.append(getattr(self.model, field) != value['!='])
                elif '>' in value:
                    filters.append(getattr(self.model, field) > value['>'])
                elif '<' in value:
                    filters.append(getattr(self.model, field) < value['<'])
                elif '>=' in value:
                    filters.append(getattr(self.model, field) >= value['>='])
                elif '<=' in value:
                    filters.append(getattr(self.model, field) <= value['<='])
                else:
                    raise ValueError(f"Unsupported operator in conditions: {value.keys()}")
            else:
                filters.append(getattr(self.model, field) == value)

        return filters

    async def async_update(self, obj_uuid: Any, update_data: Dict[str, Any]) -> Tuple[
        Optional[ModelType], Optional[SQLAlchemyError]]:
        """
        更新模型对象
        """
        if isinstance(self.db, AsyncSession):
            try:
                obj, error = await self.async_get_by_uuid(obj_uuid)
                if error:
                    return None, error
                if not obj:
                    return None, SQLAlchemyError(f"Object with uuid {obj_uuid} not found")

                for field, value in update_data.items():
                    setattr(obj, field, value)

                return obj, None
            except SQLAlchemyError as e:

                return None, e
        else:
            raise TypeError("async_update method requires an AsyncSession")

    async def sync_update(self, obj_uuid: Any, update_data: Dict[str, Any]) -> Tuple[
        Optional[ModelType], Optional[SQLAlchemyError]]:
        """
        更新模型对象
        """
        if isinstance(self.db, Session):
            try:
                obj, error = self.sync_get_by_uuid(obj_uuid)
                if error:
                    return None, error
                if not obj:
                    return None, SQLAlchemyError(f"Object with uuid {obj_uuid} not found")

                for field, value in update_data.items():
                    setattr(obj, field, value)

                return obj, None
            except SQLAlchemyError as e:

                return None, e
        else:
            raise TypeError("sync_update method requires an Session")

    async def async_patch(self, obj_uuid: Any, patch_data: Dict[str, Any]) -> Tuple[
        Optional[ModelType], Optional[SQLAlchemyError]]:
        """
        部分更新模型对象
        """
        if isinstance(self.db, AsyncSession):
            try:
                obj, error = await self.async_get_by_uuid(obj_uuid)

                if error:
                    return None, error
                if not obj:
                    return None, SQLAlchemyError(f"Object with uuid {obj_uuid} not found")

                for field, value in patch_data.items():
                    setattr(obj, field, value)
                setattr(obj, "updated_at", datetime.now())

                await self.db.flush()
                await self.db.refresh(obj)

                return obj, None

            except SQLAlchemyError as e:

                return None, e
        else:
            raise Exception("async_patch method requires an AsyncSession")

    async def sync_patch(self, obj_uuid: Any, patch_data: Dict[str, Any]) -> Tuple[
        Optional[ModelType], Optional[SQLAlchemyError]]:
        """
        部分更新模型对象
        """
        if isinstance(self.db, Session):
            try:
                obj, error = await self.sync_get_by_uuid(obj_uuid)

                if error:
                    return None, error
                if not obj:
                    return None, SQLAlchemyError(f"Object with uuid {obj_uuid} not found")

                for field, value in patch_data.items():
                    setattr(obj, field, value)
                setattr(obj, "updated_at", datetime.now())

                self.db.flush()
                self.db.refresh(obj)

                return obj, None

            except SQLAlchemyError as e:

                return None, e
        else:
            raise Exception("sync_patch method requires an Session")

    async def async_soft_delete(self, model_cls: Type, conditions: dict) -> Tuple[
        bool, Optional[SQLAlchemyError]]:
        """
        通用的软删除方法，适用于任意模型对象
        """
        if isinstance(self.db, AsyncSession):
            try:
                async with self.db as session:  # 假设 self.db 返回 AsyncSession 实例
                    # 构建查询条件
                    query = select(model_cls).where(
                        and_(*[getattr(model_cls, key) == value for key, value in conditions.items()]))
                    result = await session.execute(query)
                    exist_obj = result.scalars().first()

                    if exist_obj is None:
                        raise Exception(f"{model_cls.__name__} not found")

                    # 执行软删除操作，这里假设模型类有 deleted_at 字段
                    exist_obj.deleted_at = datetime.now()
                    await self.db.flush()

                    return True, None

            except SQLAlchemyError as e:

                return False, e
        else:
            raise Exception("async_soft_delete method requires an AsyncSession")

    def sync_soft_delete(self, model_cls: Type, conditions: dict) -> Tuple[
        bool, Optional[SQLAlchemyError]]:
        """
        通用的软删除方法，适用于任意模型对象
        """
        if isinstance(self.db, Session):
            try:
                with self.db as session:  # 假设 self.db 返回 AsyncSession 实例
                    # 构建查询条件
                    query = select(model_cls).where(
                        and_(*[getattr(model_cls, key) == value for key, value in conditions.items()]))
                    result = session.execute(query)
                    exist_obj = result.scalars().first()

                    if exist_obj is None:
                        raise Exception(f"{model_cls.__name__} not found")

                    # 执行软删除操作，这里假设模型类有 deleted_at 字段
                    exist_obj.deleted_at = datetime.now()
                    self.db.flush()

                    return True, None

            except SQLAlchemyError as e:

                return False, e
        else:
            raise TypeError("sync_soft_delete method requires an Session")

    async def async_delete(self, obj_uuid: Any) -> Tuple[bool, Optional[SQLAlchemyError]]:
        """
        删除模型对象
        """
        if isinstance(self.db, AsyncSession):
            try:
                obj, error = await self.async_get_by_uuid(obj_uuid)
                if error:
                    return False, error
                if not obj:
                    return False, SQLAlchemyError(f"Object with uuid {obj_uuid} not found")

                await self.db.delete(obj)

                return True, None
            except SQLAlchemyError as e:

                return False, e
        else:
            raise TypeError("async_delete method requires an AsyncSession")

    def sync_delete(self, obj_uuid: Any) -> Tuple[bool, Optional[SQLAlchemyError]]:
        """
        删除模型对象
        """
        if isinstance(self.db, Session):
            try:
                obj, error = self.sync_get_by_uuid(obj_uuid)
                if error:
                    return False, error
                if not obj:
                    return False, SQLAlchemyError(f"Object with uuid {obj_uuid} not found")

                self.db.delete(obj)

                return True, None
            except SQLAlchemyError as e:

                return False, e
        else:
            raise TypeError("sync_delete method requires an Session")
