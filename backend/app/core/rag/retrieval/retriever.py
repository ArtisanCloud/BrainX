from typing import Optional, list
from core.model_manager import ModelInstance
from core.rag.extractor.entity.extract_setting import ExtractSetting
from core.rag.models.document import Document
from core.splitter.fixed_text_splitter import EnhanceRecursiveCharacterTextSplitter, FixedRecursiveCharacterTextSplitter
from core.splitter.text_splitter import TextSplitter
from models.dataset import Dataset, DatasetProcessRule
from core.vector_index.base_vector_index import BaseVectorIndex


class Retriever:
    def __init__(self, vector_index: BaseVectorIndex):
        self.vector_index = vector_index

    def retrieve(self, retrival_method: str, query: str, dataset: Dataset, top_k: int,
                 score_threshold: float, reranking_model: dict) -> list[Document]:
        return self.vector_index.retrieve(retrival_method, query, dataset, top_k, score_threshold, reranking_model)

    def _get_splitter(self, processing_rule: dict,
                      embedding_model_instance: Optional[ModelInstance]) -> TextSplitter:
        if processing_rule['mode'] == "custom":
            rules = processing_rule['rules']
            segmentation = rules["segmentation"]
            max_segmentation_tokens_length = 100  # Example value, replace with actual config
            if segmentation["max_tokens"] < 50 or segmentation["max_tokens"] > max_segmentation_tokens_length:
                raise ValueError(f"Custom segment length should be between 50 and {max_segmentation_tokens_length}.")

            separator = segmentation["separator"]
            if separator:
                separator = separator.replace('\\n', '\n')

            character_splitter = FixedRecursiveCharacterTextSplitter.from_encoder(
                chunk_size=segmentation["max_tokens"],
                chunk_overlap=segmentation.get('chunk_overlap', 0),
                fixed_separator=separator,
                separators=["\n\n", "。", ". ", " ", ""],
                embedding_model_instance=embedding_model_instance
            )
        else:
            character_splitter = EnhanceRecursiveCharacterTextSplitter.from_encoder(
                chunk_size=DatasetProcessRule.AUTOMATIC_RULES['segmentation']['max_tokens'],
                chunk_overlap=DatasetProcessRule.AUTOMATIC_RULES['segmentation']['chunk_overlap'],
                separators=["\n\n", "。", ". ", " ", ""],
                embedding_model_instance=embedding_model_instance
            )

        return character_splitter
