import tempfile
import uuid
from io import BytesIO
from typing import Union, List

import requests
from langchain_community.document_loaders import UnstructuredMarkdownLoader

from app.core.rag.indexing.extractor.base import BaseDataExtractor, Block, BlockType


class MarkdownDataExtractor(BaseDataExtractor):

    def __init__(self, file_input: Union[str, BytesIO], mode: str = "paged"):
        self.file_input = file_input
        self.loader = None
        self.doc = None
        self.mode = mode

    def load(self):
        """Initialize the document based on the input."""
        if isinstance(self.file_input, BytesIO):
            # 如果输入是 BytesIO 类型，将其保存为临时文件再加载文档
            try:
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(self.file_input.getvalue())
                    tmp_file_path = tmp_file.name
                self.loader = UnstructuredMarkdownLoader(tmp_file_path, mode=self.mode)
            except Exception as e:
                raise RuntimeError(f"Failed to open the document from BytesIO: {e}")

        elif isinstance(self.file_input, str):
            if self.file_input.startswith("http://") or self.file_input.startswith("https://"):
                # 如果输入是 URL，尝试下载并加载文档
                try:
                    response = requests.get(self.file_input)
                    response.raise_for_status()  # 确保下载成功
                    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                        tmp_file.write(response.content)
                        tmp_file_path = tmp_file.name
                    self.loader = UnstructuredMarkdownLoader(tmp_file_path, mode=self.mode)
                except requests.RequestException as e:
                    raise RuntimeError(f"Failed to download the document: {e}")
                except Exception as e:
                    raise RuntimeError(f"Failed to open the downloaded document: {e}")

            else:
                # 如果输入是文件路径，直接加载 Doc
                try:
                    self.loader = UnstructuredMarkdownLoader(self.file_input, mode=self.mode)
                except Exception as e:
                    raise RuntimeError(f"Failed to open the Doc file: {e}")
        else:
            raise TypeError("file_input must be either a string or a BytesIO object.")

    def extract(self) -> List[Block]:
        # print("interface doc:", self.doc)
        blocks: list[Block] = []

        """Extract blocks of text, images, and tables from the document."""
        if not self.loader:
            self.load()

        text_content = ""
        try:

            self.doc = self.loader.load()
            # print(self.doc)
            for page in self.doc:
                blocks.append(Block(
                    block_id=str(uuid.uuid4()),
                    type=BlockType.TEXT.value,
                    text=page.page_content,
                ))
        finally:
            # Ensure the document object is closed
            pass
            # if self.doc:
            # self.doc.close()
            # self.doc = None

        return blocks
