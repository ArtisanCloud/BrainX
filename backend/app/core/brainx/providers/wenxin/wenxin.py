from app.core.brainx.interface.provider import ProviderInterface


class WenXinProvider(ProviderInterface):

    def validate_provider_credentials(self, credentials: dict) -> Exception:
        pass
