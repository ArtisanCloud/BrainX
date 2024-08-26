from enum import Enum

class VectorStoreType(Enum):
    ANALYTIC_DB = 'analytic_db'
    CHROMA = 'chroma'
    ELASTIC_SEARCH = 'elastic_search'
    FAISS = 'faiss'
    MILVUS = 'milvus'
    MY_SCALE = 'myscale'
    OPENSEARCH = 'opensearch'
    ORACLE = 'oracle'
    PGVECTOR = 'pgvector'
    QDRANT = 'qdrant'
    RELYT = 'relyt'
    TENCENT = 'tencent'
    TIDB_VECTOR = 'tidb_vector'
    WEAVIATE = 'weaviate'
