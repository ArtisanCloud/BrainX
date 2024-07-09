from contextvars import ContextVar

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.schemas.auth import auth_user_uuid_key, ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

context_user_uuid: ContextVar[str | None] = ContextVar(auth_user_uuid_key, default=None)


def get_current_user():
    # user_uuid = context_user_uuid.get()
    # print("current_user",user_uuid)
    # if user_uuid is None:
    pass


# 验证JWT令牌
def auth_user_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 解析token里的user uuid
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print(payload)
        user_uuid: str = payload.get(auth_user_uuid_key)
        if user_uuid is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    context_user_uuid.set(user_uuid)
    print("set current context user uuid from token:", context_user_uuid)
