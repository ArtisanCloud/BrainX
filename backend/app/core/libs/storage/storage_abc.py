from abc import ABC, abstractmethod
from typing import Generator, Union


class StorageABC(ABC):
    """Abstract base class for file storage systems."""

    def __init__(self, config: dict):
        """Initialize the storage system with configuration.

        Args:
            config (dict): Configuration settings for the storage system.
        """
        self.config = config

    @abstractmethod
    def save(self, filename: str, data: bytes) -> None:
        """Save data to a file in the storage system.

        Args:
            filename (str): The name of the file.
            data (bytes): The data to save.
        """
        pass

    @abstractmethod
    def load_once(self, filename: str) -> bytes:
        """Load the contents of a file as bytes.

        Args:
            filename (str): The name of the file.

        Returns:
            bytes: The file contents.
        """
        pass

    @abstractmethod
    def load_stream(self, filename: str) -> Generator[bytes, None, None]:
        """Stream the contents of a file.

        Args:
            filename (str): The name of the file.

        Returns:
            Generator[bytes, None, None]: The file contents as a stream.
        """
        pass

    @abstractmethod
    def download(self, filename: str, target_filepath: str) -> None:
        """Download a file to a specified path.

        Args:
            filename (str): The name of the file.
            target_filepath (str): The path to download the file to.
        """
        pass

    @abstractmethod
    def exists(self, filename: str) -> bool:
        """Check if a file exists in the storage system.

        Args:
            filename (str): The name of the file.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        pass

    @abstractmethod
    def delete(self, filename: str) -> None:
        """Delete a file from the storage system.

        Args:
            filename (str): The name of the file.
        """
        pass
