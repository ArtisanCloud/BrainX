from typing import List

from pydantic import BaseModel


class Log(BaseModel):
    path: str
    split: List[str]
    level: str
    keep_days: int
    console: bool
    stat: bool
