import os
from enum import Enum
from typing import List, Optional
from pydantic import AnyHttpUrl, EmailStr

from dotenv import load_dotenv
# 加载环境变量
load_dotenv()

class Settings():
    # LLM API
    OPENAI_API_BASE: str = ""
    OPENAI_API_KEY: str = ""

    # OSS Storage
    OSS_ENDPOINT: str = ""
    OSS_DRIVER: str = ""
    # aws
    AWS_KEY: str = ""
    AWS_SECRET: str = ""
    # minio
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str

    # Libs source
    POLYGON_API_KEY: str = ""
    PROJECT_NAME: str = "brain_x"
    API_PREFIX: str = "/api"
    DATABASE_URL: str
    LOG_LEVEL: str = "DEBUG"
    IS_PULL_REQUEST: bool = False
    RENDER: bool = False
    CODE_SPACES: bool = False
    CODE_SPACE_NAME: Optional[str]
    S3_BUCKET_NAME: str
    S3_ASSET_BUCKET_NAME: str
    CDN_BASE_URL: str
    VECTOR_STORE_TABLE_NAME: str = "pg_vector_store"
    SENTRY_DSN: Optional[str]
    RENDER_GIT_COMMIT: Optional[str]
    LOADER_IO_VERIFICATION_STR: str = "loaderio-e51043c635e0f4656473d3570ae5d9ec"
    SEC_EDGAR_COMPANY_NAME: str = "{ArtisanCloud}"
    SEC_EDGAR_EMAIL: EmailStr = "{dev@artisan-cloud.com}"

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    def __init__(self):
        # Initialize other attributes here if needed

        self.OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        self.POLYGON_IO_API_KEY = os.getenv("POLYGON_IO_API_KEY")

        pass

class AppEnvironment(str, Enum):
    """
    Enum for app environments.
    """

    LOCAL = "local"
    PREVIEW = "preview"
    PRODUCTION = "production"

settings = Settings()
# print(settings.DATABASE_URL)
os.environ["OPENAI_API_BASE"] = settings.OPENAI_API_BASE
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
os.environ["POLYGON_API_KEY"] = settings.POLYGON_API_KEY
