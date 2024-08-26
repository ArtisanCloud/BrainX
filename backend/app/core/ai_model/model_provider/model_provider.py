from typing import List

from app.core.ai_model.model_instance import ModelInstance


class ProviderModel:
    def __init__(self, name: str, config: dict):
        # 初始化提供商
        self.name = name
        self.config = config

    def create_instance(self, model_name: str, config: dict) -> ModelInstance:
        # 根据模型名和配置创建模型实例
        raise NotImplementedError("This method should be implemented by subclasses")

    def list_available_models(self) -> List[str]:
        # 列出可用模型
        raise NotImplementedError("This method should be implemented by subclasses")

    def get_model_info(self, model_name: str) -> dict:
        # 获取模型信息
        raise NotImplementedError("This method should be implemented by subclasses")
