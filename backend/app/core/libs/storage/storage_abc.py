from abc import ABC, abstractmethod
from datetime import datetime
from typing import Generator, Union, Any, Optional
from io import BytesIO

from pydantic import BaseModel


class ObjectResult(BaseModel):
    bucket_name: Optional[str] = None
    object_name: Optional[str] = None
    version_id: Optional[str] = None
    etag: Optional[dict] = None
    http_headers: Optional[str] = None
    last_modified: Optional[datetime] = None,
    location: str = '',


class StorageABC(ABC):
    """Abstract base class for file storage systems."""

    def __init__(self, config: dict):
        """Initialize the storage system with configuration.

        Args:
            config (dict): Configuration settings for the storage system.
        """
        self.config = config

    @abstractmethod
    def save(self,
             bucket_name: str,
             object_name: str,
             data: bytes,
             length: int,
             content_type: str = "application/octet-stream",
             metadata: dict | None = None,
             # sse: Sse | None = None,
             # progress: ProgressType | None = None,
             part_size: int = 0,
             num_parallel_uploads: int = 3,
             # tags: Tags | None = None,
             # retention: Retention | None = None,
             legal_hold: bool = False
             ) -> ObjectResult:
        """Save data to a file in the storage system.

        Args:
            bucket_name (str): The name of the bucket where the object will be stored.
            object_name (str): The name of the object to be stored.
            data (BytesIO): The data to save as a BytesIO stream.
            length (int): The length of the data in bytes.
            content_type (str, optional): The MIME type of the object. Defaults to "application/octet-stream".
            metadata (dict | None, optional): Additional metadata for the object. Defaults to None.
            part_size (int, optional): The size of each part for multipart uploads, in bytes. Defaults to 0.
            num_parallel_uploads (int, optional): The number of parallel uploads for multipart uploads. Defaults to 3.
            legal_hold (bool, optional): Whether to place a legal hold on the object. Defaults to False.

        Returns:
            Any
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
    async def check_bucket_exists(self, bucket: str) -> Exception | None:
        """Check if a bucket exists in the storage system.If not , create the bucket as the bucket name

        Args:
            bucket (str): The name of the bucket.

        Returns:
            Exception: Not None if the bucket check has exception, None otherwise.
        """
        pass

    @abstractmethod
    def delete(self, filename: str) -> None:
        """Delete a file from the storage system.

        Args:
            filename (str): The name of the file.
        """
        pass
