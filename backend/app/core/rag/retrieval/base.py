from enum import Enum


class RetrieverDriverType(Enum):
    DEFAULT = "default"
    LANGCHAIN = "langchain"
    LLAMA_INDEX = "llamaindex"

    def __str__(self):
        return self.value
