from io import BytesIO
from typing import Union

from app.utils.media import ContentType
from app.core.rag.indexing.extractor.drivers.word_doc.doc import DocDataExtractor
from app.core.rag.indexing.extractor.drivers.pdf.pdf import PDFDataExtractor
from .base import BaseDataExtractor


class DataExtractorFactory:
    @staticmethod
    def get_extractor(extractor_type: str, file_input: Union[str, BytesIO]) -> BaseDataExtractor:
        # print(f"ContentType.PDF: '{ContentType.PDF.value}'")
        # print(f"extractor_type: '{extractor_type}'")
        match extractor_type:
            # PDF files are supported
            case ContentType.PDF.value:
                return PDFDataExtractor(file_input)
            # Doc files are supported
            case (ContentType.DOC.value | ContentType.DOCX.value):
                return DocDataExtractor(file_input)
            # Excel files are supported
            case(ContentType.DOC.value | ContentType.DOCX.value):
                return ExcelDataExtractor(file_input)
            # MD files are supported
            case(ContentType.DOC.value | ContentType.DOCX.value):
                return MarkdownDataExtractor(file_input)
            # Other file types are not supported
            case _:
                raise ValueError(f"Unknown extractor type: {extractor_type}")
