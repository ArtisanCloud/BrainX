from dataclasses import field, dataclass
from enum import Enum
from typing import List, Any

from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel, Field, conint, confloat

from app.core.rag.retrieval.interface import BaseRetriever
from app.core.workflow.node.base import BaseNode
from app.core.workflow.state import GraphState
from app.models import Dataset


class SearchStrategyType(Enum):
    SEMANTIC_SEARCH = "semantic_search"
    HYBRID_SEARCH = "hybrid_search"
    FULL_TEXT_SEARCH = "full_text_search"


class KnowledgeNodeDatasetConfig(BaseModel):
    search_strategy_type: SearchStrategyType = Field(SearchStrategyType.SEMANTIC_SEARCH.value,
                                                     description="The strategy type for searching.")
    top_k: conint(ge=1, le=20) = Field(3,
                                       description="The maximum number of top k rank, default is 3, range is 1 to 20.")
    max_recalls: conint(ge=1, le=20) = Field(3,
                                             description="The maximum number of recalls, default is 3, range is 1 to 20.")
    minimum_matching_degree: confloat(ge=0.01, le=0.99) = Field(0.5,
                                                                description="The minimum matching degree, default is 0.5, range is 0.01 to 0.99.")


class KnowledgeNode(BaseNode):
    datasets: List[Dataset] = field(default_factory=list)
    config: KnowledgeNodeDatasetConfig = field(default_factory=object)
    retriever: BaseRetriever = field(default_factory=object)

    def __init__(self, node_data: dict):
        super().__init__(node_data)
        self.retriever = node_data.get("retriever", None)
        self.datasets = node_data.get("datasets", None)
        self.config = node_data.get("config", None)

    def execute(self, state: GraphState):
        super().execute(state)

        # node_list = self.context_manager.get_node_list()
        print(f"---"
              f"dataset: {self.datasets}, "
              f"inputs: {self.input_vars}"
              f"---")

        messages = self.retriever.retrieve(
            state.question,
            top_k=self.config.top_k,
            score_threshold=self.config.minimum_matching_degree)
        state.messages.append(HumanMessage(content="~~~finish knowledge node here "))

        state.messages.append(messages)

        return state

    def set_datasets(self, datasets: List[Dataset]):
        self.datasets = datasets

    def set_datasets_config(self, config: KnowledgeNodeDatasetConfig):
        self.config = config
