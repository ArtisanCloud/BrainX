from pydantic import BaseModel


class MinIO(BaseModel):
    endpoint: str
    access_key: str
    secret_key: str
    use_ssl: bool
    region: str
    bucket_name: str


class LocalStorage(BaseModel):
    storage_path: str


class AliyunOSS(BaseModel):
    endpoint: str
    access_key: str
    secret_key: str
    bucket_name: str


class AzureOSS(BaseModel):
    account_name: str
    account_key: str
    container_name: str
    bucket_name: str


class GoogleOSS(BaseModel):
    bucket_name: str


class S3OSS(BaseModel):
    endpoint: str
    access_key: str
    secret_key: str
    bucket_name: str


class Storage(BaseModel):
    driver: str
    host: str
    local_storage: LocalStorage
    minio: MinIO
    aliyun: AliyunOSS
    azure: AzureOSS
    google: GoogleOSS
    s3: S3OSS
