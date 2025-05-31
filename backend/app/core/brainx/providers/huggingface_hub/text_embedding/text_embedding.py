from collections.abc import Mapping

from pydantic import Field

from app import settings
from app.constant.ai_model.huggingface_hub import HuggingFaceHubModelID
from app.core.brainx.interface.text_embedding import TextEmbeddingModel
from langchain_huggingface import HuggingFaceEmbeddings


class HuggingFaceHubTextEmbeddingModel(TextEmbeddingModel):
    model_id: str = Field(default=HuggingFaceHubModelID.SHIBING624_TEXT2VEC_BASE_CHINESE, description="模型 ID")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate_credentials(self, credentials: Mapping) -> None:
        pass

    def get_provider_model(self) -> any:
        # 检查类变量中是否已有实例
        # print(f"Cache object address: {id(HuggingFaceHubTextEmbeddingModel._embeddings_cache)}")
        # print(f"Cache object: {HuggingFaceHubTextEmbeddingModel._embeddings_cache}")
        if HuggingFaceHubTextEmbeddingModel._embeddings_cache is None:
            print("Loading HuggingFace Embeddings...")
            # 只有在没有缓存实例时才创建新的实例
            embeddings_instance = HuggingFaceEmbeddings(
                model_name=settings.models.qa_embedding_model_name
            )
            HuggingFaceHubTextEmbeddingModel._embeddings_cache = (
                embeddings_instance  # 将实例缓存到类变量中
            )
            print("HuggingFace Embeddings loaded")

        embeddings_instance = (
            HuggingFaceHubTextEmbeddingModel._embeddings_cache
        )  # 获取缓存的实例

        # 打印缓存对象的内存地址
        # print(f"Cache object address: {id(embeddings_instance)}")

        return embeddings_instance

    def run_text_embedding(self, input_text: str) -> any:
        embeddings = self.get_provider_model()
