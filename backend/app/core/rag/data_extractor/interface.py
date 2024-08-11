from abc import ABC, abstractmethod
from typing import Tuple, List


class DataExtractorInterface(ABC):
    """
    Define the parser interface.
    """

    @abstractmethod
    def parse(self, max_text_length: int = 800, overlap: int = 50):
        raise NotImplementedError

    @abstractmethod
    def extract(self, doc: any, page: any, page_number: int) -> Tuple[List[any], List[any], List[any]]:
        raise NotImplementedError
