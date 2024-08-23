from enum import Enum

from app.core.rag.indexing.splitter.base import BaseTextSplitter
from app.core.rag.indexing.splitter.drivers.langchain.splitter import LangchainRecursiveCharacterTextSplitter
from app.core.rag.indexing.splitter.drivers.llamaindex.splitter import LlamaIndexRecursiveCharacterTextSplitter


class SplitterDriverType(Enum):
    DEFAULT = "default"
    LANGCHAIN = "langchain"
    LLAMA_INDEX = "llamaindex"

    def __str__(self):
        return self.value


class SplitterType(Enum):
    CHARACTER = "character"
    RECURSIVE_CHARACTER = "recursive_character"
    TOKEN = "token"


class TextSplitterFactory:

    @staticmethod
    def get_splitter(splitter_driver_type: SplitterDriverType) -> BaseTextSplitter:

        match splitter_driver_type.value:

            case SplitterDriverType.LANGCHAIN.value:
                return LangchainRecursiveCharacterTextSplitter(
                    chunk_size=800,
                    chunk_overlap=50,
                    # chunk_size=segmentation["max_tokens"],
                    # chunk_overlap=chunk_overlap,
                    # separator="\n\n", # process_rule segment id
                    separators=["\n\n", "。", ". ", " ", ""],
                    keep_separator="end",
                )

            case SplitterDriverType.LLAMA_INDEX.value:
                return LlamaIndexRecursiveCharacterTextSplitter()

            case _:
                raise ValueError(f"Unknown splitter type: {splitter_driver_type}")
