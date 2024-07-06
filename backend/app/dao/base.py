from datetime import datetime

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Any, TypeVar, Generic, Optional, Type, Tuple

# 定义 ModelType 类型变量，限定为 SQLAlchemy 的 DeclarativeMeta
ModelType = TypeVar('ModelType', bound=DeclarativeMeta)


class BaseDAO(Generic[ModelType]):
    def __init__(self, db: AsyncSession, model: Type[ModelType]):
        self.db = db
        self.model = model

    async def create(self, obj: ModelType) -> Tuple[Optional[ModelType], Optional[Exception]]:
        """
        创建新的模型对象
        """
        # print(obj)
        try:
            self.db.add(obj)
            await self.db.commit()

            await self.db.refresh(obj)  # 刷新对象以获取数据库中的最新状态
            return obj, None
        except SQLAlchemyError as e:
            await self.db.rollback()
            return None, e

    async def create_many(self, objs: List[ModelType]) -> Tuple[Optional[List[ModelType]], Optional[Exception]]:
        """
        创建新的模型对象
        """
        try:
            self.db.add_all(objs)
            await self.db.commit()
            return objs, None
        except SQLAlchemyError as e:
            await self.db.rollback()
            return None, e

    async def get_by_id(self, obj_id: Any) -> Tuple[Optional[ModelType], Optional[Exception]]:
        """
        根据 ID 获取模型对象
        """
        try:
            result = await self.db.execute(select(self.model).filter(self.model.id == obj_id))
            return result.scalar_one_or_none(), None
        except SQLAlchemyError as e:
            return None, e

    async def get_by_uuid(self, uuid: str) -> Tuple[Optional[ModelType], Optional[Exception]]:
        """
        根据 UUID 获取模型对象
        """
        try:
            result = await self.db.execute(select(self.model).filter(self.model.uuid == uuid))
            return result.scalar_one_or_none(), None
        except SQLAlchemyError as e:
            return None, e

    async def get_objects_by_conditions(self, conditions: Dict[str, Any]) -> Tuple[
        Optional[List[ModelType]], Optional[Exception]]:
        """
        根据给定的条件查询模型对象
        """
        try:
            query = select(self.model)
            filters = self._build_filters(conditions)

            if filters:
                query = query.filter(and_(*filters))

            # 打印生成的 SQL 查询语句
            query_str = str(query)
            print(conditions)
            print(f"Generated SQL query: {query_str}")

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

    async def update(self, obj_id: Any, update_data: Dict[str, Any]) -> Tuple[Optional[ModelType], Optional[Exception]]:
        """
        更新模型对象
        """
        try:
            obj, error = await self.get_by_id(obj_id)
            if error:
                return None, error
            if not obj:
                return None, Exception(f"Object with id {obj_id} not found")

            for field, value in update_data.items():
                setattr(obj, field, value)

            await self.db.commit()
            return obj, None
        except SQLAlchemyError as e:
            await self.db.rollback()
            return None, e

    async def patch(self, obj_id: Any, patch_data: Dict[str, Any]) -> Tuple[Optional[ModelType], Optional[Exception]]:
        """
        部分更新模型对象
        """
        try:
            obj, error = await self.get_by_id(obj_id)
            if error:
                return None, error
            if not obj:
                return None, Exception(f"Object with id {obj_id} not found")

            for field, value in patch_data.items():
                setattr(obj, field, value)

            await self.db.commit()
            return obj, None
        except SQLAlchemyError as e:
            await self.db.rollback()
            return None, e

    async def soft_delete(self, model_cls: Type, conditions: dict) -> Tuple[bool, Optional[Exception]]:
        """
        通用的软删除方法，适用于任意模型对象
        """
        try:
            async with self.db as session:  # 假设 self.db 返回 AsyncSession 实例
                # 构建查询条件
                query = select(model_cls).where(and_(*[getattr(model_cls, key) == value for key, value in conditions.items()]))
                result = await session.execute(query)
                exist_obj = result.scalars().first()

                if exist_obj is None:
                    raise Exception(f"{model_cls.__name__} not found")

                # 执行软删除操作，这里假设模型类有 deleted_at 字段
                exist_obj.deleted_at = datetime.now()
                await session.commit()
                return True, None

        except SQLAlchemyError as e:
            await session.rollback()
            return False, e

    async def delete(self, obj_id: Any) -> Tuple[bool, Optional[Exception]]:
        """
        删除模型对象
        """
        try:
            obj, error = await self.get_by_id(obj_id)
            if error:
                return False, error
            if not obj:
                return False, Exception(f"Object with id {obj_id} not found")

            await self.db.delete(obj)
            await self.db.commit()
            return True, None
        except SQLAlchemyError as e:
            await self.db.rollback()
            return False, e
