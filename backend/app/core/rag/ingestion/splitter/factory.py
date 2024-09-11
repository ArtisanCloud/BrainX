from enum import Enum

from app.core.rag import FrameworkDriverType
from app.core.rag.ingestion.splitter.base import BaseTextSplitter
from app.core.rag.ingestion.splitter.drivers.langchain.splitter import LangchainRecursiveCharacterTextSplitter
from app.core.rag.ingestion.splitter.drivers.llamaindex.splitter import LlamaIndexRecursiveCharacterTextSplitter



class SplitterType(Enum):
    CHARACTER = "character"
    RECURSIVE_CHARACTER = "recursive_character"
    TOKEN = "token"


class TextSplitterFactory:

    @staticmethod
    def get_splitter(splitter_driver_type: FrameworkDriverType) -> BaseTextSplitter:

        match splitter_driver_type.value:

            case FrameworkDriverType.LANGCHAIN.value:
                return LangchainRecursiveCharacterTextSplitter(
                    chunk_size=800,
                    chunk_overlap=50,
                    # chunk_size=segmentation["max_tokens"],
                    # chunk_overlap=chunk_overlap,
                    # separator="\n\n", # process_rule segment id
                    separators=["\n\n", "。", ". ", " ", ""],
                    keep_separator="end",
                    length_function=len,
                )

            case FrameworkDriverType.LLAMA_INDEX.value:
                return LlamaIndexRecursiveCharacterTextSplitter()

            case _:
                raise ValueError(f"Unknown splitter type: {splitter_driver_type}")
