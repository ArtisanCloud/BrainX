from abc import ABC, abstractmethod


class DataExtractorInterface(ABC):
    """
    Define the parser interface.
    """

    @abstractmethod
    def parse(self):
        raise NotImplementedError

    @abstractmethod
    def extract(self):
        raise NotImplementedError


