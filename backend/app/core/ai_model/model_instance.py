from typing import Any


class ModelInstance:
    def __init__(self,  provider_model, config: dict):
        # 初始化模型实例

        self.provider_model = provider_model
        self.config = config


    def run_inference(self, input_data: Any) -> Any:
        # 运行推理任务
        raise NotImplementedError("This method should be implemented by subclasses")


    def update_config(self, new_config: dict):
        # 更新模型配置
        self.config.update(new_config)
