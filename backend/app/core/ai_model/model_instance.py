from typing import Any

from app.core.ai_model.drivers.interface.ai_model import AIModel


class ModelInstance:
    def __init__(self, model: AIModel, config: dict = None):
        # 初始化模型实例

        self.model = model

    def run_inference(self, input_data: Any) -> Any:
        # 运行推理任务
        pass

    def run_text_embedding(self, input_text: str) -> Any:
        # 运行向量化
        pass
