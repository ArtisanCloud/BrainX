from typing import Optional

from pydantic import constr

from app.models.rag.dataset import Dataset, ImportType
from app.schemas.base import Pagination, ResponsePagination, BaseSchema, BaseObjectSchema


class DatasetSchema(BaseObjectSchema):
    tenant_uuid: Optional[str] = None
    created_user_by: Optional[str] = None
    updated_user_by: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_published: Optional[bool] = None
    import_type: Optional[int] = None
    driver_type: Optional[int] = None
    embedding_model: Optional[str] = None
    embedding_model_provider: Optional[str] = None

    @classmethod
    def from_orm(cls, obj: Dataset):
        base = super().from_orm(obj)
        # print(base)
        return cls(
            **base,
            tenant_uuid=obj.tenant_uuid,
            created_user_by=str(obj.created_user_by),
            updated_user_by=str(obj.updated_user_by),
            name=obj.name,
            description=obj.description,
            is_published=obj.is_published,
            import_type=obj.import_type,
            driver_type=obj.driver_type,
            embedding_model=obj.embedding_model,
            embedding_model_provider=obj.embedding_model_provider
        )

class RequestGetDatasetList(BaseSchema):
    pagination: Optional[Pagination] = None


class ResponseGetDatasetList(BaseSchema):
    data: list[DatasetSchema]
    pagination: ResponsePagination


class RequestCreateDataset(DatasetSchema):
    name: constr(min_length=1)
    description: constr(min_length=1)

class ResponseCreateDataset(BaseSchema):
    dataset: DatasetSchema


class RequestPatchDataset(DatasetSchema):
    pass


class ResponsePatchDataset(BaseSchema):
    dataset: DatasetSchema


class ResponseDeleteDataset(BaseSchema):
    result: bool


def make_dataset(dataset: DatasetSchema) -> Dataset:
    return Dataset(
        tenant_uuid=dataset.tenant_uuid,
        created_user_by=dataset.created_user_by,
        updated_user_by=dataset.updated_user_by,
        name=dataset.name,
        description=dataset.description,
        avatar_url=dataset.avatar_url,
        is_published=dataset.is_published,
        import_type=dataset.import_type,
        driver_type=dataset.driver_type,
        embedding_model=dataset.embedding_model,
        embedding_model_provider=dataset.embedding_model_provider,
    )
