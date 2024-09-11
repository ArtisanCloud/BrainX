import tempfile
import uuid
from io import BytesIO
from typing import Union, List

import requests
from langchain_community.document_loaders import UnstructuredExcelLoader

from app.core.rag.ingestion.extractor.base import BaseDataExtractor, Block, BlockType


class ExcelDataExtractor(BaseDataExtractor):

    def __init__(self, file_input: Union[str, BytesIO]):
        self.file_input = file_input
        self.loader = None
        self.doc = None

    def load(self):
        """Initialize the document based on the input."""
        if isinstance(self.file_input, BytesIO):
            # 如果输入是 BytesIO 类型，将其保存为临时文件再加载文档
            try:
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(self.file_input.getvalue())
                    tmp_file_path = tmp_file.name
                self.loader = UnstructuredExcelLoader(tmp_file_path)
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
                    self.loader = UnstructuredExcelLoader(tmp_file_path)
                except requests.RequestException as e:
                    raise RuntimeError(f"Failed to download the document: {e}")
                except Exception as e:
                    raise RuntimeError(f"Failed to open the downloaded document: {e}")

            else:
                # 如果输入是文件路径，直接加载 Doc
                try:
                    self.loader = UnstructuredExcelLoader(self.file_input)
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

        blocks = []
        text_content = ""
        try:

            self.doc = self.loader.load()
            print(len(self.doc))
            for sheet in self.doc:
                blocks.append(Block(
                    block_id=str(uuid.uuid4()),
                    type=BlockType.TEXT.value,
                    text=sheet.page_content,
                ))
        finally:
            # Ensure the document object is closed
            pass

        return blocks
