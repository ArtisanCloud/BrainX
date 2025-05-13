from typing import  List, Optional

from pydantic import BaseModel


class ElasticSearch(BaseModel):
    enable: bool = False
    hosts: List[str] = ["127.0.0.1:9200"]
    username: str = "kibana_user"
    password: str = "your_password"
    index_name: str = "brain_x_log"


class Loki(BaseModel):
    enable: bool = False
    url: str = "http://localhost:3100/loki/api/v1/push"


class ExtraConfig(BaseModel):
    elasticsearch: Optional[ElasticSearch] = None
    loki: Optional[Loki] = None


class Log(BaseModel):
    file: bool = True
    console: bool = True
    path: str = "logs"
    split: List[str]
    level: str
    interval: int = 1
    keep_days: int = 7
    stat: bool
    exc_info: bool = False
    extra: ExtraConfig = ExtraConfig()
