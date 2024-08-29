from abc import ABC

class ProviderInterface(ABC):

    def verify_provider_credentials(self, credentials: dict) -> Exception:
        raise NotImplementedError("This method should be implemented by subclasses")
