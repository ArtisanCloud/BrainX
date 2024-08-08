from app.utils.media import ContentType
from .drivers.doc import DocDataExtractor
from .drivers.pdf import PDFDataExtractor
from .interface import DataExtractorInterface


class DataExtractorFactory:
    @staticmethod
    def get_extractor(extractor_type: str) -> DataExtractorInterface:
        match extractor_type:
            # PDF files are supported
            case ContentType.PDF:
                return PDFDataExtractor("")
            # Doc files are supported
            case (ContentType.DOC | ContentType.DOCX):
                return DocDataExtractor("")
            # Other file types are not supported
            case _:
                raise ValueError(f"Unknown extractor type: {extractor_type}")
