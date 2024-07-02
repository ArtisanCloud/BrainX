from abc import ABC, abstractmethod
from typing import Any, List, Dict


class BaseStoring(ABC):
    """
    Abstract base class for various types of storage.
    """

    @abstractmethod
    def connect_vector_db(self, connection_params: Dict[str, Any]) -> None:
        """
        Connect to the vector database with specified parameters.

        Args:
            connection_params (Dict[str, Any]): Parameters needed to establish connection.
        """
        pass

    @abstractmethod
    def close_vector_db(self) -> None:
        """
        Close the connection to the vector database.
        """
        pass

    @abstractmethod
    def create_vector_index(self, index_name: str, index_params: Dict[str, Any]) -> None:
        """
        Create an index for vectors in the vector database.

        Args:
            index_name (str): Name of the index to create.
            index_params (Dict[str, Any]): Parameters for creating the index.
        """
        pass

    @abstractmethod
    def search_vector_index(self, query_vector: List[float], top_k: int) -> List[str]:
        """
        Search for vectors in the vector index.

        Args:
            query_vector (List[float]): Vector query to search for.
            top_k (int): Number of top results to retrieve.

        Returns:
            List[str]: List of keys or IDs of vectors matching the query.
        """
        pass

    @abstractmethod
    def store_document(self, doc_id: str, document: Dict[str, Any]) -> None:
        """
        Store a document with its identifier.

        Args:
            doc_id (str): The unique identifier for the document.
            document (Dict[str, Any]): The document data to be stored.
        """
        pass

    @abstractmethod
    def store_index(self, index_key: str, index_data: Any) -> None:
        """
        Store index data associated with a key.

        Args:
            index_key (str): The key to associate with the index data.
            index_data (Any): The index data to be stored.
        """
        pass

    @abstractmethod
    def store_chat_message(self, chat_id: str, message: Dict[str, Any]) -> None:
        """
        Store a chat message associated with a chat identifier.

        Args:
            chat_id (str): The identifier for the chat or conversation.
            message (Dict[str, Any]): The chat message data to be stored.
        """
        pass

    @abstractmethod
    def store_key_value(self, key: str, value: Any) -> None:
        """
        Store a key-value pair.

        Args:
            key (str): The key of the key-value pair.
            value (Any): The value to be stored.
        """
        pass

    @abstractmethod
    def custom_store(self, key: str, data: Any) -> None:
        """
        Customized storage method for specific storage needs.

        Args:
            key (str): The key or identifier for the data.
            data (Any): The data to be stored.
        """
        pass

    @abstractmethod
    def store_vector(self, key: str, vector: List[float]) -> None:
        """
        Store a vector representation associated with a key.

        Args:
            key (str): The identifier key for the vector.
            vector (List[float]): The vector data to be stored.
        """
        pass

    # Additional methods specific to storing implementation
    @abstractmethod
    def create_collection(self, collection_name: str) -> None:
        """
        Create a new collection or namespace for storing data.

        Args:
            collection_name (str): The name of the collection.
        """
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str) -> None:
        """
        Delete an entire collection or namespace.

        Args:
            collection_name (str): The name of the collection to delete.
        """
        pass

    @abstractmethod
    def search_by_metadata(self, key: str, value: Any) -> List[str]:
        """
        Search for data IDs based on metadata key-value pair.

        Args:
            key (str): The metadata key to search by.
            value (Any): The value associated with the metadata key.

        Returns:
            List[str]: A list of IDs matching the search criteria.
        """
        pass

    @abstractmethod
    def delete_data_by_ids(self, data_ids: List[str]) -> None:
        """
        Delete data entries based on their IDs.

        Args:
            data_ids (List[str]): List of IDs of data entries to delete.
        """
        pass

    # Other generic storing methods can be defined here
