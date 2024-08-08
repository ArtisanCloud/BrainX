from abc import ABC, abstractmethod
from typing import Sequence, Tuple, Optional, List, Iterator

class StoreInterface(ABC):
    """
    Define the base key-value store interface.
    """

    @abstractmethod
    def mget(self, key: Sequence[str]) -> List[Optional[bytes]]:
        """
        Get the contents of multiple keys.

        Args:
            key (Sequence[str]): The list of keys to retrieve.

        Returns:
            List[Optional[bytes]]: A list of values corresponding to the keys, or None if a key does not exist.
        """
        pass

    @abstractmethod
    def mset(self, key_value_pairs: Sequence[Tuple[str, bytes]]) -> None:
        """
        Set the contents of multiple keys.

        Args:
            key_value_pairs (Sequence[Tuple[str, bytes]]): A list of key-value pairs to set.
        """
        pass

    @abstractmethod
    def mdelete(self, key: Sequence[str]) -> None:
        """
        Delete multiple keys.

        Args:
            key (Sequence[str]): The list of keys to delete.
        """
        pass

    @abstractmethod
    def yield_keys(self, prefix: Optional[str] = None) -> Iterator[str]:
        """
        Yield all keys in the store, optionally filtering by a prefix.

        Args:
            prefix (Optional[str]): The prefix to filter keys, if any.

        Returns:
            Iterator[str]: An iterator over keys in the store.
        """
        pass
