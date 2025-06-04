from typing import List

from pydantic import Field, BaseModel


class ModelLoadBalanceConfig(BaseModel):
    enable: bool = Field(default=False, description="是否启用模型负载均衡")
    configs: List = Field(default=[], description="模型负载均衡配置")
