import os

import yaml

from pydantic import BaseModel

from app.config.api import Api, JWT
from app.config.baidu import BaiduQianfan
from app.config.cache import Cache
from app.config.celery import CeleryConfig
from app.config.database import Database
from app.config.kimi import Kimi
from app.config.log import Log
from app.config.ollama import OLLAMA
from app.config.openai import OpenAI
from app.config.openapi import OpenAPI
from app.config.qa_model import Models
from app.config.server import Server
from app.config.storage import Storage
from app.config.test import Test
from app.config.vectore_store import VectorStore


class Polygon(BaseModel):
    api_key: str


class Sentry(BaseModel):
    dsn: str
    environment: str
    release: str
    sample_rate: float


class Settings(BaseModel):
    server: Server
    api: Api
    openapi: OpenAPI
    jwt: JWT
    log: Log
    test: Test
    database: Database
    cache: Cache
    task: CeleryConfig
    models: Models
    vector_store: VectorStore
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
    openapi=OpenAPI(**config['openapi']),
    database=Database(**config['database']),
    cache=Cache(**config['cache']),
    task=CeleryConfig(**config['task']),
    models=Models(**config['models']),
    vector_store=VectorStore(**config['vector_store']),
    log=Log(**config['log']),
    test=Test(**config['test']),
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
