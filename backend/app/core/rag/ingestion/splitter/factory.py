from enum import Enum

from app.core.rag.ingestion.splitter.base import BaseTextSplitter
from app.core.rag.ingestion.splitter.drivers.langchain.splitter import LangchainRecursiveCharacterTextSplitter


class SplitterType(Enum):
    CHARACTER = "character"
    RECURSIVE_CHARACTER = "recursive_character"
    TOKEN = "token"


class TextSplitterFactory:

    @staticmethod
    def get_splitter() -> BaseTextSplitter:
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
