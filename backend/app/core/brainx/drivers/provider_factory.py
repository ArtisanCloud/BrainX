from typing import Type, Dict
from app.constant.ai_model.provider import ProviderID
from app.core.brainx.interface.provider import ProviderInterface
from app.core.brainx.providers.huggingface_hub.huggingface_hub import HuggingFaceHubProvider
from app.core.brainx.providers.openai.openai import OpenAIProvider
from app.core.brainx.providers.wenxin.wenxin import WenXinProvider


class ProviderFactory:
    tenant_uuid: str

    _provider_map: Dict[str, Type[ProviderInterface]] = {
        ProviderID.HUGGINGFACE_HUB.value: HuggingFaceHubProvider,
        ProviderID.OPENAI.value: OpenAIProvider,
        ProviderID.WENXIN.value: WenXinProvider,
        # 可以在这里继续添加其他 LLM 提供者
    }

    def __init__(self, tenant_uuid: str):
        self.tenant_uuid = tenant_uuid

    def get_provider_instance(self, provider_id: str) -> ProviderInterface:
        init_params = {
            "tenant_uuid": self.tenant_uuid,
            "provider_id": provider_id,
            "provider_name": provider_id,
        }

        provider_class = ProviderFactory._provider_map[provider_id]
        if provider_class is None:
            raise ValueError(f"Provider {provider_id} not found")

        return provider_class(**init_params)

    def provider_credentials_validate(self, provider_id: str, credentials: dict) -> dict:
        provider = self.get_provider_instance(provider_id)

        exception = provider.validate_provider_credentials(credentials)
        if exception:
            raise exception

        return credentials
