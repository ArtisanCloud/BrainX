from typing import Optional

from app.core.brainx.interface.provider import ProviderInterface


class HuggingFaceHubProvider(ProviderInterface):
    def validate_provider_credentials(self, credentials: dict) -> Optional[Exception]:
        pass
