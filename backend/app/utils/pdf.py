import fitz  # PyMuPDF
import base64

class PDFParser:
    def __init__(self, file_path=None, base64_data=None):
        if file_path:
            self.doc = self._open_file(file_path)
        elif base64_data:
            self.doc = self._open_base64(base64_data)
        else:
            raise ValueError("Either file_path or base64_data must be provided")

    def _open_file(self, file_path):
        try:
            return fitz.open(file_path)
        except Exception as e:
            raise ValueError("Cannot open file. It might not be a valid PDF.") from e

    def _open_base64(self, base64_data):
        try:
            pdf_data = base64.b64decode(base64_data)
            return fitz.open(stream=pdf_data, filetype="pdf")
        except Exception as e:
            raise ValueError("Cannot decode base64 data. It might not be a valid PDF.") from e

    def extract_text(self):
        text = []
        for page_num in range(self.doc.page_count):
            page = self.doc.load_page(page_num)
            text.append(page.get_text())
        return "\n".join(text)

    def close(self):
        self.doc.close()