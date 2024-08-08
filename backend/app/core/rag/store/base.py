from enum import Enum


class StoreDriverType(Enum):
    DEFAULT = "default"
    LANGCHAIN = "langchain"
    LLAMA_INDEX = "llamaindex"

    def __str__(self):
        return self.value
