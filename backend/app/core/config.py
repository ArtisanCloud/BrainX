import os
from enum import Enum
from typing import List

import yaml

from pydantic import BaseModel


class AppEnvironment(str, Enum):
    LOCAL = "local"
    PREVIEW = "preview"
    PRODUCTION = "production"


class Server(BaseModel):
    version: str
    project_name: str
    host: str
    port: int
    max_bytes: int
    cors_origins: List[str]
    worker_count: int
    environment: str
    server_render: bool


class JWT(BaseModel):
    jwt_secret: str
    expire_in: int


class Api(BaseModel):
    api_prefix: str
    openapi_prefix: str
    request_timeout: int


class Database(BaseModel):
    url: str
    table_name_vector_store: str


class Redis(BaseModel):
    url: str


class Cache(BaseModel):
    redis: Redis


class Models(BaseModel):
    qa_embedding_model_name: str
    visual_search_model_name: str
    visual_query_model_name: str


class Log(BaseModel):
    path: str
    split: List[str]
    level: str
    keep_days: int
    console: bool
    stat: bool


class OpenAI(BaseModel):
    llm_name: str
    api_base: str
    api_key: str
    request_timeout: int


class BaiduQianfan(BaseModel):
    api_key: str
    secret_key: str
    request_timeout: int


class Kimi(BaseModel):
    llm_name: str
    api_base: str
    api_key: str
    request_timeout: int


class OLLAMA(BaseModel):
    url: str


class Polygon(BaseModel):
    api_key: str


class Sentry(BaseModel):
    dsn: str
    environment: str
    release: str
    sample_rate: float


class MinIO(BaseModel):
    endpoint: str
    access_key: str
    secret_key: str
    use_ssl: bool
    region: str


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
    local_storage: LocalStorage
    minio: MinIO
    aliyun: AliyunOSS
    azure: AzureOSS
    google: GoogleOSS
    s3: S3OSS


class Settings(BaseModel):
    server: Server
    api: Api
    jwt: JWT
    database: Database
    cache: Cache
    models: Models
    openai: OpenAI
    baidu_qianfan: BaiduQianfan
    kimi: Kimi
    ollama: OLLAMA
    polygon: Polygon
    sentry: Sentry
    storage: Storage


# Load the YAML file into a Python object
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Create a Settings object from the YAML data
settings = Settings(
    server=Server(**config['server']),
    jwt=JWT(**config['jwt']),
    api=Api(**config['api']),
    database=Database(**config['database']),
    cache=Cache(**config['cache']),
    models=Models(**config['models']),
    log=Log(**config['log']),
    openai=OpenAI(**config['openai']),
    baidu_qianfan=BaiduQianfan(**config['baidu_qianfan']),
    kimi=Kimi(**config['kimi']),
    ollama=OLLAMA(**config['ollama']),
    polygon=Polygon(**config['polygon']),
    sentry=Sentry(**config['sentry']),
    storage=Storage(**config['storage'])
)

# Access the settings
print(settings.server.version)
os.environ["OPENAI_API_BASE"] = settings.openai.api_base
os.environ["OPENAI_API_KEY"] = settings.openai.api_key
os.environ["QIANFAN_AK"] = settings.baidu_qianfan.api_key
os.environ["QIANFAN_SK"] = settings.baidu_qianfan.secret_key
# print(os.environ)
os.environ["POLYGON_API_KEY"] = settings.polygon.api_key
os.environ["TOKENIZERS_PARALLELISM"] = "false"
# ...
