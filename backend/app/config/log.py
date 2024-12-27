from typing import Dict, List

from pydantic import BaseModel


class ElasticSearch(BaseModel):
    enable: bool = False
    hosts: List[str] = ["127.0.0.1:9200"]
    username: str = "kibana_user"
    password: str = "your_password"
    index_name: str = "brain_x_log"


class Log(BaseModel):
    path: str
    split: List[str]
    level: str
    interval: int = 1
    keep_days: int = 7
    console: bool = True
    stat: bool
    exc_info: bool = False
    extra: Dict[str, ElasticSearch] = {}
