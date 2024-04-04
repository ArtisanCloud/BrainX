
from llama_index.core import VectorStoreIndex
from llama_index.core import get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor


def generate_query_engine(vector_store, storage_context):

    index = VectorStoreIndex.from_vector_store(
        vector_store,
        storage_context=storage_context
    )

    # configure retriever
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=1,
    )

    # configure response synthesizer
    response_synthesizer = get_response_synthesizer()

    # assemble query engine
    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.5)],
    )

    return query_engine
