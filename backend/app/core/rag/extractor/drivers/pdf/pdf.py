import uuid
from io import BytesIO
from typing import Tuple, List, Any, Union

import fitz
import requests

from app.core.rag.extractor.base import BaseDataExtractor, Block, BlockType
from app.core.rag.extractor.drivers.pdf.lib import rect_to_bbox, compare_block


class PDFDataExtractor(BaseDataExtractor):

    def __init__(self, file_input: Union[str, BytesIO]):
        self.file_input = file_input
        self.doc = None

    def load(self):
        """Initialize the document based on the input."""
        if isinstance(self.file_input, BytesIO):
            # 如果输入是 BytesIO 类型，直接加载 PDF
            try:
                self.doc = fitz.open(stream=self.file_input, filetype="pdf")
            except Exception as e:
                raise RuntimeError(f"Failed to open the PDF from BytesIO: {e}")

        elif isinstance(self.file_input, str):
            if self.file_input.startswith("http://") or self.file_input.startswith("https://"):
                # 如果输入是 URL，尝试下载并加载 PDF
                try:
                    response = requests.get(self.file_input)
                    response.raise_for_status()
                    self.doc = fitz.open(stream=BytesIO(response.content), filetype="pdf")
                except requests.RequestException as e:
                    raise RuntimeError(f"Failed to download the PDF: {e}")
            else:
                # 如果输入是文件路径，直接加载 PDF
                try:
                    self.doc = fitz.open(self.file_input)
                except Exception as e:
                    raise RuntimeError(f"Failed to open the PDF file: {e}")
        else:
            raise TypeError("file_input must be either a string or a BytesIO object.")

    def extract(self) -> List[Block]:
        # print("interface doc:", self.doc)
        blocks: list[Block] = []

        """Extract blocks of text, images, and tables from the document."""
        if self.doc is None:
            self.load()

        try:
            for page_number in range(len(self.doc)):
                page = self.doc.load_page(page_number)
                page_blocks = self._extract_block_from_content(page, page_number)
                blocks.extend(page_blocks)

        finally:
            # Ensure the document object is closed
            if self.doc:
                self.doc.close()
                self.doc = None

        return blocks

    def _extract_block_from_content(self, page: fitz.Page, page_number: int) -> List[Block]:
        blocks: List[Block] = []

        # Extract text blocks
        for block in page.get_text("blocks"):
            if block[6] == 0:  # 0 indicates text block
                bbox = [float(coord) for coord in block[:4]]
                blocks.append(Block(
                    # block_id=str(uuid.uuid4()),
                    type=BlockType.TEXT.value,
                    text=block[4],
                    rect=bbox,
                    page_number=page_number,
                ))

        # Extract images
        # see pro code

        # Extract tables (assuming you have a method to extract tables)
        # see pro code

        # Sort blocks by bbox's y0 coordinate
        blocks = sorted(blocks, key=compare_block)

        return blocks
