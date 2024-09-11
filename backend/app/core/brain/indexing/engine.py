from llama_index.core import StorageContext, VectorStoreIndex, ServiceContext, get_response_synthesizer, Settings
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from llama_index.llms.openai import OpenAI

from app.core.brain.base import LLMModel
from app.core.brain.indexing.pg_vector import get_vector_store_singleton
from app.core.brain.llm.llamaindex import get_ollama_llm
from app.config.config import settings


def bind_llm(llm: str, temperature=0.5):
    # print(llm)
    Settings.llm = None

    mdl_llm = OpenAI(
        temperature=0.5,
        model=llm,
        streaming=False,
        api_key=settings.openai.api_key,
        api_base=settings.openai.api_base
    )
    match llm:
        case (
        LLMModel.BAIDU_QIANFAN_QIANFAN_BLOOMZ_7B_COMPRESSED.value
        | LLMModel.BAIDU_ERNIE_3_D_5_8K.value
        | LLMModel.BAIDU_ERNIE_4_D_0_8K.value
        | LLMModel.BAIDU_ERNIE_Speed_128K.value
        | LLMModel.BAIDU_ERNIE_Lite_8K.value
        ):
            mdl_llm = get_ollama_llm(llm, temperature, streaming=False)
        case LLMModel.OLLAMA_13B_ALPACA_16K.value:
            # print("match:", llm, LLMModel.OLLAMA_13B_ALPACA_16K)
            mdl_llm = get_ollama_llm(llm, temperature, streaming=False)
        case LLMModel.OLLAMA_GEMMA_2B.value:
            # print("match:", llm, LLMModel.OLLAMA_GEMMA_2B)
            mdl_llm = get_ollama_llm(llm, temperature, streaming=False)

    print("llm", mdl_llm)
    # return mdl_llm
    Settings.llm = mdl_llm


def bind_embed_model():
    mdl_embedding = HuggingFaceEmbedding(
        model_name=settings.models.qa_embedding_model_name
    )

    # Settings.embed_model = mdl_embedding
    return mdl_embedding


def get_service_context(llm: str) -> ServiceContext:
    # bind_llm(llm)
    mdl_embedding = bind_embed_model()

    service_context = ServiceContext.from_defaults(
        embed_model=mdl_embedding,
    )
    return service_context


def generate_storage_context(vector_store) -> StorageContext:
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    return storage_context


async def generate_query_engine(llm):
    query_embedding_table = settings.database.table_name_vector_store
    vector_store, _ = get_vector_store_singleton(query_embedding_table)
    storage_context = generate_storage_context(vector_store)

    service_context = get_service_context(llm)

    index = VectorStoreIndex.from_vector_store(
        vector_store,
        storage_context=storage_context,
        service_context=service_context
    )

    # configure retrieval
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=1,
    )

    # configure response synthesizer
    response_synthesizer = get_response_synthesizer()

    # assemble query robot_chat
    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.5)],
    )

    return query_engine
