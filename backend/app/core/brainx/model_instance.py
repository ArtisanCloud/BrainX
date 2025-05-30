from typing import Dict, Iterator, Tuple, Any

from app.core.brainx.entity.provider_bundle import ProviderModelBundle
from app.core.brainx.entity.provider_config import ProviderConfiguration
from app.core.brainx.interface.llm import LLM
from app.models import App


class ModelInstance:
    configuration: ProviderConfiguration

    def __init__(self, model_bundle: ProviderModelBundle, model: str):
        # 初始化模型实例
        self.model_bundle = model_bundle
        self.model = model

    def llm_stream(
            self,
            query: Dict,
            temperature: float = 0.5,
            input_variables=list[str],
            template: str = "",
            **kwargs: Any,
    ) -> Tuple[Iterator | None, Exception | None]:

        if not isinstance(self.model_bundle.model_type_instance, LLM):
            return None, Exception("Model type instance is not LargeLanguageModel")

        return self.model_bundle.model_type_instance.stream(
            query=query,
            temperature=temperature,
            input_variables=input_variables,
            template=template,
        )

    def llm_invoke(
            self,
            query: Any,
            temperature: float = 0.5,
            input_variables=list[str],
            template: str = "",
            output_schemas: Any = None,
            **kwargs: Any,
    ) -> Tuple[Any | None, Exception | None]:
        if not isinstance(self.model_bundle.model_type_instance, LLM):
            return None, Exception("Model type instance is not LargeLanguageModel")

        return self.model_bundle.model_type_instance.invoke(
            query=query,
            temperature=temperature,
            input_variables=input_variables,
            template=template,
            output_schemas=output_schemas,
        )

    def llm_chat_completion(
            self,
            query: Dict,
            temperature: float = 0.5,
            app: App = None,
            session_id: str = "",
            **kwargs: Any,
    ) -> Tuple[str | None, Exception | None]:
        if not isinstance(self.model_bundle.model_type_instance, LLM):
            return None, Exception("Model type instance is not LargeLanguageModel")

        return self.model_bundle.model_type_instance.chat_completion(
            query=query,
            temperature=temperature,
            app=app,
            session_id=session_id,
        )

    def llm_chat_stream(
            self,
            question: Dict,
            app: App = None,
            temperature: float = 0.5,
            session_id: str = "",
            **kwargs: Any,
    ) -> Tuple[Iterator | None, Exception | None]:

        if not isinstance(self.model_bundle.model_type_instance, LLM):
            return None, Exception("Model type instance is not LargeLanguageModel")

        return self.model_bundle.model_type_instance.chat_stream(
            question=question,
            temperature=temperature,
            app=app,
            session_id=session_id,
        )
