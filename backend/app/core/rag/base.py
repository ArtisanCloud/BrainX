from app.config.config import settings

from app.constant.ai_model.huggingface_hub import HuggingFaceHubModelID
from app.constant.ai_model.provider import ProviderID
from app.core.ai_model.drivers.langchain.factory import ModelProviderFactory
from app.core.ai_model.model_instance import ModelInstance
from app.core.rag import FrameworkDriverType
from app.core.rag.ingestion.factory import IndexingFactory
from app.core.rag.retrieval.factory import RetrieverFactory
from app.core.rag.retrieval.interface import BaseRetriever
from app.core.rag.synthesis.factory import AgentExecutorFactory

def create_text_embedding_model():
    text_embedding_model = ModelProviderFactory.create_text_embedding_provider(
        ProviderID.HUGGINGFACE_HUB,
        HuggingFaceHubModelID.SHIBING624_TEXT2VEC_BASE_CHINESE.value,
    )
    embedding_model_instance = ModelInstance(model=text_embedding_model)
    return embedding_model_instance

def create_indexer(embedding_model_instance: ModelInstance = None):
    return IndexingFactory.get_indexer(
        FrameworkDriverType(settings.agent.framework_driver),
        None,
        embedding_model_instance,
        None,
        None,
    )

def create_retriever(
    collection_name: str = settings.agent.vector_store_collection, embedding_model_instance: ModelInstance = None
) -> BaseRetriever:
    return RetrieverFactory.get_retriever(
        FrameworkDriverType(settings.agent.framework_driver),
        collection_name=collection_name,
        embedding_model_instance=embedding_model_instance,
    )

def create_agent_executor(
    llm: str,
    temperature: float = 0.5,
    streaming: bool = False,
):
    return AgentExecutorFactory.get_agent_executor(
        FrameworkDriverType(settings.agent.framework_driver),
        llm,
        temperature=temperature,
        streaming=streaming,
    )