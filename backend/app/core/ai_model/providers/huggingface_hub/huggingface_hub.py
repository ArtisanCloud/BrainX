from app.core.ai_model.drivers.interface.provider import ProviderInterface


class HuggingFaceHubProvider(ProviderInterface):

    def validate_provider_credentials(self, credentials: dict) -> Exception:
        pass
