from abc import abstractmethod, ABC
from typing import List

from app.core.rag.ingestion.extractor.base import Block, BlockType
from app.models.rag.document_node import DocumentNode


class BaseTextSplitter(ABC):

    @abstractmethod
    def split_nodes(self, nodes: List[DocumentNode]) -> list[DocumentNode]:
        """Split text into multiple components."""
        pass

    @classmethod
    def merge_blocks_into_text(cls, blocks: List[Block]) -> str:
        """
        将 Blocks 合并成一个长文本，根据需要插入换行符。

        :param blocks: List of Block objects.
        :return: Merged text.
        """
        merged_text = ""
        join = "\n"
        for block in blocks:
            if block.type == BlockType.TEXT.value:
                # 在文本块之间插入换行符
                merged_text += block.text.strip() + join
            elif block.type == BlockType.IMAGE.value:
                # 处理图片的通配符
                pass
            elif block.type == BlockType.TABLE.value:
                # 处理表格块
                placeholder_table = f"{block.table}"
                merged_text += placeholder_table + join
        return merged_text
