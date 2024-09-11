from app.schemas.base import BaseSchema


class ResponseAuthToken(BaseSchema):
    tokenType: str = ""
    expiresIn: int = -1
    accessToken: str = ""
    refreshToken: str = ""
