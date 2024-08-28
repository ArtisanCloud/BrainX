from app.core.ai_model.model_provider.model_provider import ModelProvider


class WenXinProvider(ModelProvider):

    def verify_provider_credentials(self, credentials: dict) -> Exception:
        pass
