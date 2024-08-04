from typing import Optional

from pydantic import constr

from app.models.app.app import App
from app.schemas.base import Pagination, ResponsePagination, BaseSchema, BaseObjectSchema


class AppSchema(BaseObjectSchema):
    tenant_uuid: Optional[str] = None
    created_user_by: Optional[str] = None
    updated_user_by: Optional[str] = None
    app_model_config_uuid: Optional[str] = None
    workflow_uuid: Optional[str] = None
    name: Optional[str] = None
    status: Optional[int] = None
    type: Optional[int] = None
    mode: Optional[str] = None
    description: Optional[str] = None
    persona: Optional[int] = None
    avatar_url: Optional[str] = None
    is_public: Optional[str] = None

    @classmethod
    def from_orm(cls, obj: App):
        base = super().from_orm(obj)
        # print(base)
        return cls(
            **base,
            tenant_uuid=str(obj.tenant_uuid),
            created_user_by=str(obj.created_user_by),
            updated_user_by=str(obj.updated_user_by),
            app_model_config_uuid=str(obj.app_model_config_uuid),
            workflow_uuid=obj.workflow_uuid,
            name=obj.name,
            status=obj.status,
            type=obj.type,
            mode=obj.mode,
            description=obj.description,
            avatar_url=obj.avatar_url
        )


class RequestGetAppList(BaseSchema):
    pagination: Optional[Pagination] = None


class ResponseGetAppList(BaseSchema):
    data: list[AppSchema]
    pagination: ResponsePagination

    # def __init__(self, data: list[AppSchema], pagination: ResponsePagination):
    #
    # super().__init__(pagination.limit, pagination.page, pagination.sort, pagination.total_rows,
    #                  pagination.total_pages)
    # self.data = data


class RequestCreateApp(AppSchema):
    name: constr(min_length=1)
    description: constr(min_length=1)


class ResponseCreateApp(BaseSchema):
    app: AppSchema


class ResponseGetApp(BaseSchema):
    data: AppSchema

class RequestPatchApp(AppSchema):
    pass


class ResponsePatchApp(BaseSchema):
    app: AppSchema


class ResponseDeleteApp(BaseSchema):
    result: bool


def make_app(app: AppSchema) -> App:
    return App(
        tenant_uuid=app.tenant_uuid,
        created_user_by=app.created_user_by,
        updated_user_by=app.updated_user_by,
        app_model_config_uuid=app.app_model_config_uuid,
        workflow_uuid=app.workflow_uuid,
        name=app.name,
        status=app.status,
        type=app.type,
        mode=app.mode,
        description=app.description,
        avatar_url=app.avatar_url,
        is_public=app.is_public,
    )
