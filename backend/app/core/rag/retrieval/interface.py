from abc import ABC, abstractmethod
from typing import List
from app.models import Document


class RetrieverInterface(ABC):
    """
    Define the retriever interface.
    """

    @abstractmethod
    def retrieve(self, query: str) -> List[Document]:
        """
        Retrieve documents based on a given query.

        Args:
            query (str): The query string used for retrieving documents.

        Returns:
            List[Document]: A list of documents that match the query.
        """
        pass
