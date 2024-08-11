from io import BytesIO
from typing import Tuple, List

import fitz

from app.core.rag.data_extractor.interface import DataExtractorInterface


class PDFDataExtractor(DataExtractorInterface):

    def __init__(self, file_data: BytesIO):
        self.file_data = file_data
        self.document = None

    def parse(self, max_text_length: int = 800, overlap: int = 50):
        try:
            print(self.file_data)
        except Exception as e:
            raise ValueError(f"Error opening PDF file: {e}")

    def extract(self, doc: any, page: any, page_number: int) -> Tuple[List[any], List[any], List[any]]:

        return [], [], []
