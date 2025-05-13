from datetime import datetime

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta, Session
from sqlalchemy.exc import IntegrityError

from typing import List, Dict, Any, TypeVar, Generic, Optional, Type, Tuple, Sequence

from app.config.config import UTC

# 定义 ModelType 类型变量，限定为 SQLAlchemy 的 DeclarativeMeta
ModelType = TypeVar('ModelType', bound=DeclarativeMeta)


class BaseDAO(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], async_db: AsyncSession = None, sync_db: Session = None):
        self.async_db = async_db
        self.sync_db = sync_db
        self.model = model

    async def async_create(self, obj: ModelType) -> Tuple[
        Optional[ModelType], Optional[Exception]]:
        """
        创建新的模型对象
        """
        if isinstance(self.async_db, AsyncSession):
            # print(obj)
            try:
                self.async_db.add(obj)
                await self.async_db.flush()
                await self.async_db.refresh(obj)  # 刷新对象以获取数据库中的最新状态

                return obj, None
            except Exception as e:
                return None, e
        else:
            return None, Exception("a_create method requires an AsyncSession")

    def sync_create(self, obj: ModelType) -> Tuple[
        Optional[ModelType], Optional[Exception]]:
        """
        创建新的模型对象
        """
        if isinstance(self.sync_db, Session):
            try:
                self.sync_db.add(obj)
                self.sync_db.flush()
                self.sync_db.refresh(obj)  # 刷新对象以获取数据库中的最新状态

                return obj, None
            except Exception as e:
                return None, e
        else:
            return None, Exception("sync_create method requires an Session")

    def sync_upsert(self, obj: ModelType, uid_key: str) -> Tuple[Optional[ModelType], Optional[Exception]]:
        """
        先查询是否存在该记录：
        - 如果存在，则更新
        - 如果不存在，则创建
        :param obj: SQLAlchemy 模型对象
        :param uid_key: 用于唯一标识的字段（如 'id', 'uuid' 等）
        """
        if not hasattr(obj, uid_key):
            return None, ValueError(f"Model {obj.__class__.__name__} 没有 `{uid_key}` 字段")

        uid_value = getattr(obj, uid_key)  # 获取唯一标识的值
        if isinstance(self.sync_db, Session):
            try:
                # 先查询是否存在
                existing_obj, error = self.sync_get_by_uuid(uid_value)
                if error is None or existing_obj is not None:
                    return self.sync_update(existing_obj, obj)  # 传入数据库对象，而不是 uid
                else:
                    return self.sync_create(obj)

            except IntegrityError as e:
                return None, e
        else:
            return None, Exception("sync_upsert method requires a Session")

    async def async_upsert(self, obj: ModelType, uid_key: str) -> Tuple[Optional[ModelType], Optional[Exception]]:
        """
        先查询是否存在该记录：
        - 如果存在，则更新
        - 如果不存在，则创建
        :param obj: SQLAlchemy 模型对象
        :param uid_key: 用于唯一标识的字段（如 'id', 'uuid' 等）
        """
        if not hasattr(obj, uid_key):
            return None, ValueError("unknown_field")

        uid_value = getattr(obj, uid_key)  # 获取唯一标识的值

        try:
            # 先查询是否存在
            existing_obj, error = await self.async_get_by_uuid(uid_value)
            if error is None and existing_obj is not None:
                update_data = {k: v for k, v in obj.__dict__.items() if not k.startswith('_')}
                return await self.async_update(uid_value, update_data)  # 传入数据库对象，而不是 uid
            else:
                return await self.async_create(obj)

        except IntegrityError as e:
            return None, e

    async def async_create_many(self, objs: List[ModelType]) -> Tuple[
        Optional[List[ModelType]], Optional[Exception]]:
        """
        创建新的模型对象
        """
        if isinstance(self.async_db, AsyncSession):
            try:
                self.async_db.add_all(objs)
                await self.async_db.flush()
                # print(objs)
                return objs, None
            except Exception as e:

                return None, e
        else:
            return None, Exception("async_create_many method requires an AsyncSession")

    def sync_create_many(self, objs: List[ModelType]) -> Tuple[
        Optional[List[ModelType]], Optional[Exception]]:
        """
        创建新的模型对象
        """
        if isinstance(self.sync_db, Session):
            try:
                self.sync_db.add_all(objs)
                self.sync_db.flush()
                # print(objs)
                return objs, None
            except Exception as e:
                return None, e
        else:
            return None, Exception("sync_create_many method requires an Session")

    async def async_get_by_uuid(self, uuid: str) -> Tuple[Optional[ModelType], Optional[Exception]]:
        """
        根据 UUID 获取模型对象
        """
        if isinstance(self.async_db, AsyncSession):
            try:
                result = await self.async_db.execute(select(self.model).filter(self.model.uuid == uuid))
                return result.scalar_one_or_none(), None
            except Exception as e:
                return None, e
        else:
            return None, Exception("async_get_by_uuid method requires an AsyncSession")

    def sync_get_by_uuid(self, uuid: str) -> Tuple[Optional[ModelType], Optional[Exception]]:
        """
        根据 UUID 获取模型对象
        """
        if isinstance(self.sync_db, Session):
            try:
                result = self.sync_db.execute(select(self.model).filter(self.model.uuid == uuid))
                return result.scalar_one_or_none(), None
            except Exception as e:
                return None, e
        else:
            return None, Exception("sync_get_by_uuid method requires an Session")

    async def async_get_objects_by_conditions(self, conditions: Dict[str, Any]) -> Tuple[
        Optional[Sequence[ModelType]], Optional[Exception]]:
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

            result = await self.async_db.execute(query)
            objects = result.scalars().all()
            return objects, None
        except Exception as e:
            return None, e

    def sync_get_objects_by_conditions(
            self, conditions: Dict[str, Any]
    ) -> Tuple[Optional[Sequence[ModelType]], Optional[Exception]]:
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

            result = self.sync_db.execute(query)
            objects = result.scalars().all()
            return objects, None
        except Exception as e:
            return None, e

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
        Optional[ModelType], Optional[Exception]]:
        """
        更新模型对象
        """
        if isinstance(self.async_db, AsyncSession):
            try:
                obj, error = await self.async_get_by_uuid(obj_uuid)
                if error:
                    return None, error
                if not obj:
                    return None, Exception(f"Object with uuid {obj_uuid} not found")

                for field, value in update_data.items():
                    setattr(obj, field, value)

                return obj, None
            except Exception as e:

                return None, e
        else:
            return None, Exception("async_update method requires an AsyncSession")

    def sync_update(self, obj_uuid: Any, update_data: Dict[str, Any]) -> Tuple[
        Optional[ModelType], Optional[Exception]]:
        """
        更新模型对象
        """
        if isinstance(self.sync_db, Session):
            try:
                obj, error = self.sync_get_by_uuid(obj_uuid)
                if error:
                    return None, error
                if not obj:
                    return None, Exception(f"Object with uuid {obj_uuid} not found")

                for field, value in update_data.items():
                    setattr(obj, field, value)

                return obj, None
            except Exception as e:

                return None, e
        else:
            return None, Exception("sync_update method requires an Session")

    async def async_patch(self, obj_uuid: Any, patch_data: Dict[str, Any]) -> Tuple[
        Optional[ModelType], Optional[Exception]]:
        """
        部分更新模型对象
        """
        if isinstance(self.async_db, AsyncSession):
            try:
                obj, error = await self.async_get_by_uuid(obj_uuid)

                if error:
                    return None, error
                if not obj:
                    return None, Exception(f"Object with uuid {obj_uuid} not found")

                for field, value in patch_data.items():
                    setattr(obj, field, value)
                setattr(obj, "updated_at", datetime.now(UTC))

                await self.async_db.flush()
                await self.async_db.refresh(obj)

                return obj, None

            except Exception as e:

                return None, e
        else:
            return None, Exception("async_patch method requires an AsyncSession")

    def sync_patch(self, obj_uuid: Any, patch_data: Dict[str, Any]) -> Tuple[
        Optional[ModelType], Optional[Exception]]:
        """
        部分更新模型对象
        """
        if isinstance(self.sync_db, Session):
            try:
                obj, error = self.sync_get_by_uuid(obj_uuid)

                if error:
                    return None, error
                if not obj:
                    return None, Exception(f"Object with uuid {obj_uuid} not found")

                for field, value in patch_data.items():
                    setattr(obj, field, value)
                setattr(obj, "updated_at", datetime.now(UTC))

                self.sync_db.flush()
                self.sync_db.refresh(obj)

                return obj, None

            except Exception as e:

                return None, e
        else:
            return None, Exception("sync_patch method requires an Session")

    async def async_soft_delete(self, model_cls: Type, conditions: dict) -> Tuple[
        bool, Optional[Exception]]:
        """
        通用的软删除方法，适用于任意模型对象
        """
        if isinstance(self.async_db, AsyncSession):
            try:
                async with self.async_db as session:  # 假设 self.async_db 返回 AsyncSession 实例
                    # 构建查询条件
                    query = select(model_cls).where(
                        and_(*[getattr(model_cls, key) == value for key, value in conditions.items()]))
                    result = await session.execute(query)
                    exist_obj = result.scalars().first()

                    if exist_obj is None:
                        return False, Exception(f"{model_cls.__name__} not found")

                    # 执行软删除操作，这里假设模型类有 deleted_at 字段
                    exist_obj.deleted_at = datetime.now(UTC)
                    await self.async_db.flush()

                    return True, None

            except Exception as e:

                return False, e
        else:
            return False, Exception("async_soft_delete method requires an AsyncSession")

    def sync_soft_delete(self, model_cls: Type, conditions: dict) -> Tuple[
        bool, Optional[Exception]]:
        """
        通用的软删除方法，适用于任意模型对象
        """
        if isinstance(self.sync_db, Session):
            try:
                with self.sync_db as session:  # 假设 self.async_db 返回 AsyncSession 实例
                    # 构建查询条件
                    query = select(model_cls).where(
                        and_(*[getattr(model_cls, key) == value for key, value in conditions.items()]))
                    result = session.execute(query)
                    exist_obj = result.scalars().first()

                    if exist_obj is None:
                        return False, Exception(f"{model_cls.__name__} not found")

                    # 执行软删除操作，这里假设模型类有 deleted_at 字段
                    exist_obj.deleted_at = datetime.now(UTC)
                    self.async_db.flush()

                    return True, None

            except Exception as e:

                return False, e
        else:
            return False, Exception("sync_soft_delete method requires an Session")

    async def async_delete(self, obj_uuid: Any) -> Tuple[bool, Optional[Exception]]:
        """
        删除模型对象
        """
        if isinstance(self.async_db, AsyncSession):
            try:
                obj, error = await self.async_get_by_uuid(obj_uuid)
                if error:
                    return False, error
                if not obj:
                    return False, Exception(f"Object with uuid {obj_uuid} not found")

                await self.async_db.delete(obj)

                return True, None
            except Exception as e:

                return False, e
        else:
            return False, Exception("async_delete method requires an AsyncSession")

    def sync_delete(self, obj_uuid: Any) -> Tuple[bool, Optional[Exception]]:
        """
        删除模型对象
        """
        if isinstance(self.sync_db, Session):
            try:
                obj, error = self.sync_get_by_uuid(obj_uuid)
                if error:
                    return False, error
                if not obj:
                    return False, Exception(f"Object with uuid {obj_uuid} not found")

                self.async_db.delete(obj)

                return True, None
            except Exception as e:

                return False, e
        else:
            return False, Exception("sync_delete method requires an Session")
