from abc import ABC


class ProviderInterface(ABC):

    def validate_provider_credentials(self, credentials: dict) -> Exception:
        raise NotImplementedError("This method should be implemented by subclasses")
