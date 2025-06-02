import base64

from sqlalchemy.orm import Session

from app.core.libs import rsa
from app.core.libs.rsa import get_tenant_private_key_path
from app.dao.tenant.tenant import TenantDAO


def encrypt_content(sync_db: Session, tenant_uuid: str, content: str):
    tenant_dao = TenantDAO(sync_db=sync_db)
    tenant, exception = tenant_dao.sync_get_by_uuid(tenant_uuid)
    if exception:
        raise exception
    if not tenant:
        raise ValueError(f"Tenant with uuid {tenant_uuid} not found")

    encrypted_content = rsa.rsa_encrypt(tenant.encrypted_public_key, content)

    return base64.b64encode(encrypted_content).decode()


def desensitized_content(token: str):
    if not token:
        return token
    if len(token) <= 8:
        return "*" * 20
    return token[:6] + "*" * 12 + token[-2:]


def decrypt_content(tenant_uuid: str, content: str) -> str:
    return rsa.rsa_decrypt(tenant_uuid, base64.b64decode(content))


def batch_decrypt_content(tenant_uuid: str, contents: list[str]):
    rsa_key, cipher_rsa = rsa.get_decrypt_decoding(tenant_uuid)

    return [rsa.decrypt_content_with_decoding(base64.b64decode(content), rsa_key, cipher_rsa) for content in contents]


def get_decrypt_decoding(tenant_uuid: str):
    return rsa.get_decrypt_decoding(tenant_uuid)


def decrypt_content_with_decoding(content: str, rsa_key, cipher_rsa):
    return rsa.decrypt_content_with_decoding(base64.b64decode(content), rsa_key, cipher_rsa)
