from typing import Dict, Any


# 定义ModelConfig类
class ModelConfig:
    def __init__(self, model_id: str, config: Dict[str, Any]):
        self.model_id = model_id
        self.config = config

    def get_config(self) -> Dict[str, Any]:
        # 返回模型的配置
        return self.config

    def update_config(self, new_config: Dict[str, Any]):
        # 更新模型的配置
        self.config.update(new_config)

    def validate_config(self) -> bool:
        # 验证当前配置的有效性
        pass


class ProviderConfig:
    def __init__(self, provider_id: str, config: Dict[str, Any]):
        self.provider_id = provider_id
        self.config = config

    def get_config(self) -> Dict[str, Any]:
        # 返回供应商的配置
        return self.config

    def update_config(self, new_config: Dict[str, Any]):
        # 更新供应商的配置
        self.config.update(new_config)

    def validate_config(self) -> bool:
        # 验证供应商配置的有效性
        pass
