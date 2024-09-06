from datetime import datetime, timezone, timedelta

from app.openapi.models.platform import Platform
from app.schemas.auth import AccessTokenSchema, ALGORITHM, auth_user_uuid_key, auth_tenant_uuid_key
from jose import jwt


def sign_token(platform: Platform, secret_key, expires_in) -> AccessTokenSchema:
    print("current sign token key:", secret_key)
    now = datetime.now(timezone.utc)
    access_token_payload = {
        "auth_access_key": str(platform.access_key),
        'name': platform.name,
        'exp': now + timedelta(seconds=expires_in)
    }
    access_token = jwt.encode(access_token_payload, secret_key, algorithm=ALGORITHM)

    refresh_token_payload = {
        'sub': str(platform.access_key),
        'exp': now + timedelta(seconds=(30 * 24 * 3600 + expires_in))
    }
    refresh_token = jwt.encode(refresh_token_payload, secret_key, algorithm=ALGORITHM)

    return AccessTokenSchema(token_type="Bearer", access_token=access_token, refresh_token=refresh_token,
                             expires_in=expires_in)
