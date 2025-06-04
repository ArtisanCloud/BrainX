from typing import Optional

from app.core.brainx.interface.provider import ProviderInterface


class HuggingFaceHubProvider(ProviderInterface):
    def validate_credentials(
            self,
            tenant_uuid: str,
            user_uuid: str,
            provider_id: str,
            credentials: dict
    ) -> Optional[Exception]:
        pass
