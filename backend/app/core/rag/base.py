from app.config.config import settings

from app.constant.ai_model.huggingface_hub import HuggingFaceHubModelID
from app.constant.ai_model.provider import ProviderID
from app.core.brainx.drivers.factory import ModelProviderFactory

from app.core.brainx.entity.provider_bundle import ProviderModelBundle
from app.core.brainx.model_instance import ModelInstance
from app.core.rag.ingestion.factory import IndexingFactory
from app.core.rag.retrieval.factory import RetrieverFactory
from app.core.rag.retrieval.interface import BaseRetriever


def create_text_embedding_model():
    text_embedding_model = ModelProviderFactory.create_text_embedding_provider(
        provider_id=ProviderID.HUGGINGFACE_HUB,
        model_id=HuggingFaceHubModelID.SHIBING624_TEXT2VEC_BASE_CHINESE.value,
    )
    model_bundle = ProviderModelBundle(model=text_embedding_model)
    embedding_model_instance = ModelInstance(model_bundle=model_bundle, model=ProviderID.HUGGINGFACE_HUB.value)
    return embedding_model_instance


def create_indexer(embedding_model_instance: ModelInstance = None):
    return IndexingFactory.get_indexer(
        None,
        embedding_model_instance,
        None,
        None,
    )


def create_retriever(
        collection_name: str = settings.agent.vector_store_collection, embedding_model_instance: ModelInstance = None
) -> BaseRetriever:
    return RetrieverFactory.get_retriever(
        collection_name=collection_name,
        embedding_model_instance=embedding_model_instance,
    )

# def create_agent_executor(
#         llm: str,
#         temperature: float = 0.5,
#         streaming: bool = False,
# ) -> BaseAgentExecutor:
#     return AgentExecutorFactory.get_agent_executor(
#         llm,
#         temperature=temperature,
#         streaming=streaming,
#     )
