from typing import Type

from app.core.rag.store.base import StoreDriverType
from app.core.rag.store.drivers.langchain.store import LangchainStore
from app.core.rag.store.drivers.llamaindex.store import LLamaIndexStore


class StoreFactory:
    @staticmethod
    def get_store(store_type: StoreDriverType) -> Type[BaseStore]:
        match store_type:
            case StoreDriverType.LLAMA_INDEX:
                return LLamaIndexStore()
            case StoreDriverType.LANGCHAIN:
                return LangchainStore()
            case _:
                raise ValueError(f"Unknown store type: {store_type}")
