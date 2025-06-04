from typing import Optional

from app.core.brainx.interface.provider import ProviderInterface


class WenXinProvider(ProviderInterface):

    def validate_credentials(
            self,
            tenant_uuid: str,
            user_uuid: str,
            provider_id: str,
            credentials: dict,
            model_type: str = None,
            model_id: str = None,
    ) -> Exception:
        pass
