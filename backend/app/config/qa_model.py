from pydantic import BaseModel


class Models(BaseModel):
    qa_embedding_model_name: str
    visual_search_model_name: str
    visual_query_model_name: str
