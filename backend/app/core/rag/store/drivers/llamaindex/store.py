from typing import Sequence, Tuple, Optional, List, Iterator
from app.core.rag.store.interface import StoreInterface


class LLamaIndexStore(StoreInterface):
    """
    Implementation of BaseStore for LLamaIndex storage.
    """

    def __init__(self):
        """
        Initialize the LLamaIndexStore.
        """
        # Initialize LLamaIndex storage resources
        self.store = {}  # This is a placeholder; replace with actual LLamaIndex store initialization

    def mget(self, key: Sequence[str]) -> List[Optional[bytes]]:
        """
        Get the contents of multiple keys from LLamaIndex store.

        Args:
            key (Sequence[str]): The list of keys to retrieve.

        Returns:
            List[Optional[bytes]]: A list of values corresponding to the keys, or None if a key does not exist.
        """
        return [self.store.get(k) for k in key]

    def mset(self, key_value_pairs: Sequence[Tuple[str, bytes]]) -> None:
        """
        Set the contents of multiple keys in LLamaIndex store.

        Args:
            key_value_pairs (Sequence[Tuple[str, bytes]]): A list of key-value pairs to set.
        """
        for k, v in key_value_pairs:
            self.store[k] = v

    def mdelete(self, key: Sequence[str]) -> None:
        """
        Delete multiple keys from LLamaIndex store.

        Args:
            key (Sequence[str]): The list of keys to delete.
        """
        for k in key:
            if k in self.store:
                del self.store[k]

    def yield_keys(self, prefix: Optional[str] = None) -> Iterator[str]:
        """
        Yield all keys in the LLamaIndex store, optionally filtering by a prefix.

        Args:
            prefix (Optional[str]): The prefix to filter keys, if any.

        Returns:
            Iterator[str]: An iterator over keys in the store.
        """
        if prefix:
            return (k for k in self.store if k.startswith(prefix))
        return iter(self.store.keys())
