from dataclasses import field, dataclass
from enum import Enum
from typing import List, Any

from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel, Field, conint, confloat

from app.core.workflow.node.base import BaseNode
from app.core.workflow.state import GraphState


class SearchStrategyType(Enum):
    SEMANTIC_SEARCH = "semantic_search"
    HYBRID_SEARCH = "hybrid_search"
    FULL_TEXT_SEARCH = "full_text_search"


class KnowledgeNodeDatasetConfig(BaseModel):
    dataset_uuid: str = Field(..., description="The UUID of the dataset.")
    search_strategy_type: SearchStrategyType = Field(SearchStrategyType.SEMANTIC_SEARCH.value,
                                                     description="The strategy type for searching.")
    max_recalls: conint(ge=1, le=20) = Field(3,
                                             description="The maximum number of recalls, default is 3, range is 1 to 20.")
    minimum_matching_degree: confloat(ge=0.01, le=0.99) = Field(0.5,
                                                                description="The minimum matching degree, default is 0.5, range is 0.01 to 0.99.")


class KnowledgeNode(BaseNode):
    datasets: List[KnowledgeNodeDatasetConfig] = field(default_factory=list)

    def __init__(self, node_data: dict):
        super().__init__(node_data)

    def execute(self, state: GraphState):
        super().execute(state)

        # node_list = self.context_manager.get_node_list()
        print(f"---"
              # f"dataset: {self.datasets}, "
              # f"inputs: {node_list}"
              f"---")

        message = self.llm.invoke(state.question)
        state.messages.append(HumanMessage(content="~~~finish knowledge node here "))
        state.messages.append(message)

        return state
