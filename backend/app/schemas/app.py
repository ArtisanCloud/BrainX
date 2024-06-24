from typing import Optional

from pydantic import constr

from app.models.app import App
from app.schemas.base import Pagination, ResponsePagination, BaseSchema, BaseObjectSchema


class AppSchema(BaseObjectSchema):
    user_id: Optional[int] = None
    parent_id: Optional[int] = None
    app_model_config_uuid: Optional[str] = None
    name: Optional[str] = None
    status: Optional[int] = None
    type: Optional[int] = None
    description: Optional[str] = None
    persona_prompt: Optional[str] = None
    avatar_url: Optional[str] = None

    @classmethod
    def from_orm(cls, obj: App):
        base = super().from_orm(obj)
        # print(base)
        return cls(
            **base,
            user_id=obj.user_id,
            parent_id=obj.parent_id,
            model_uuid=obj.app_model_config_uuid,
            name=obj.name,
            status=obj.status,
            type=obj.type,
            description=obj.description,
            persona_prompt=obj.persona_prompt,
            avatar_url=obj.avatar_url
        )

class RequestGetAppList:
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


class RequestPatchApp(AppSchema):
    pass


class ResponsePatchApp(BaseSchema):
    app: AppSchema

class ResponseDeleteApp(BaseSchema):
    result: bool


def make_app(app: AppSchema) -> App:
    return App(
        user_id=app.user_id,
        parent_id=app.parent_id,
        model_config_uuid=app.app_model_config_uuid,
        name=app.name,
        status=app.status,
        type=app.type,
        description=app.description,
        persona_prompt=app.persona_prompt,
        avatar_url=app.avatar_url,
    )
