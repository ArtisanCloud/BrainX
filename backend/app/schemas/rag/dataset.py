from typing import Annotated, Optional, List

from pydantic import constr, Field

from app.models.rag.dataset import Dataset
from app.schemas.base import Pagination, ResponsePagination, BaseSchema, BaseObjectSchema
from app.utils.datetime import datetime_format


class DatasetSchema(BaseObjectSchema):
    tenant_uuid: Optional[str] = None
    created_user_by: Optional[str] = None
    updated_user_by: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    avatar_url: Optional[str] = None
    is_published: Optional[bool] = None
    import_type: Optional[int] = None
    driver_type: Optional[int] = None
    word_count: Optional[int] = None
    token_count: Optional[int] = None
    embedding_model: Optional[str] = None
    embedding_model_provider: Optional[str] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None

    # extra info
    with_app_connected: Optional[bool] = None

    @classmethod
    def from_orm(cls, obj: Dataset):
        base = super().from_orm(obj)
        return cls(
            **base,
            tenant_uuid=str(obj.tenant_uuid),
            created_user_by=str(obj.created_user_by),
            updated_user_by=str(obj.updated_user_by),
            name=obj.name,
            description=obj.description,
            avatar_url=obj.avatar_url,
            is_published=obj.is_published,
            import_type=obj.import_type,
            driver_type=obj.driver_type,
            embedding_model=obj.embedding_model,
            embedding_model_provider=obj.embedding_model_provider,
            createdAt=str(obj.created_at.strftime(datetime_format)),
            updatedAt=str(obj.updated_at.strftime(datetime_format)),
        )


class RequestGetDatasetList(BaseSchema):
    app_uuid: Optional[str] = None
    pagination: Optional[Pagination] = None


class ResponseGetDatasetList(BaseSchema):
    data: list[DatasetSchema]
    pagination: ResponsePagination


class ResponseGetDataset(BaseSchema):
    data: DatasetSchema


class RequestCreateDataset(DatasetSchema):
    name: Annotated[str, Field(min_length=1)]
    # name: constr(min_length=1)
    # description: constr(min_length=1)


class ResponseCreateDataset(BaseSchema):
    dataset: DatasetSchema


class RequestPatchDataset(DatasetSchema):
    pass


class ResponsePatchDataset(BaseSchema):
    dataset: DatasetSchema


class ResponseDeleteDataset(BaseSchema):
    result: bool


class RequestGetDatasetListWithApp(BaseSchema):
    only_connected: bool
    app_uuid: str


class ResponseGetDatasetListWithApp(BaseSchema):
    data: list[DatasetSchema]


class RequestDatasetSyncApps(BaseSchema):
    app_uuid: str
    connect_dataset_uuids: List[str]
    disconnect_dataset_uuids: List[str]


class ResponseDatasetSyncApps(BaseSchema):
    datasets: List[Dataset]


class RequestDatasetConnectApps(BaseSchema):
    app_uuid: str
    dataset_uuids: List[str]


class ResponseDatasetConnectApps(BaseSchema):
    result: bool


class RequestDatasetDisconnectApps(BaseSchema):
    app_uuid: str
    dataset_uuids: List[str]


class ResponseDatasetDisconnectApps(BaseSchema):
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
