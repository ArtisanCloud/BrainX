from app.core.ai_model.drivers.interface.provider import ProviderInterface


class WenXinProvider(ProviderInterface):

    def verify_provider_credentials(self, credentials: dict) -> Exception:
        pass
