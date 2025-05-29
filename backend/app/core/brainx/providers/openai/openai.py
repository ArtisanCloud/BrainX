from app.core.brainx.interface.provider import ProviderInterface


class OpenAIProvider(ProviderInterface):

    def validate_provider_credentials(self, credentials: dict) -> Exception:
        pass
