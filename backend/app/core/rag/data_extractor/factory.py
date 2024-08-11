from io import BytesIO

from app.utils.media import ContentType
from .drivers.doc import DocDataExtractor
from .drivers.pdf import PDFDataExtractor
from .interface import DataExtractorInterface


class DataExtractorFactory:
    @staticmethod
    def get_extractor(extractor_type: str, file_data: BytesIO) -> DataExtractorInterface:
        # print(f"ContentType.PDF: '{ContentType.PDF.value}'")
        # print(f"extractor_type: '{extractor_type}'")
        match extractor_type:
            # PDF files are supported
            case ContentType.PDF.value:
                return PDFDataExtractor("")
            # Doc files are supported
            case (ContentType.DOC.value | ContentType.DOCX.value):
                return DocDataExtractor("")
            # Other file types are not supported
            case _:
                raise ValueError(f"Unknown extractor type: {extractor_type}")
