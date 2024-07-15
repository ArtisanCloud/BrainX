import fitz

from app.core.rag.data_extractor.base import BaseExtractor


class PDFExtractor(BaseExtractor):
    def __init__(self, file_path):
        self.file_path = file_path
        self.document = None

    def parse(self):
        try:
            self.document = fitz.open(self.file_path)
        except Exception as e:
            raise ValueError(f"Error opening PDF file: {e}")

    def extract(self):
        if not self.document:
            raise ValueError("Document not parsed. Call `parse` method first.")

        text = ""
        for page_num in range(self.document.page_count):
            page = self.document.load_page(page_num)
            text += page.get_text()

        return text