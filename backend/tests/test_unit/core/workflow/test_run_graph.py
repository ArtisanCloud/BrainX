import uuid
import pytest

from app import settings
from app.core.workflow.graph import create_graph_from_json
from app.core.workflow.node.base import NodeType
from app.core.workflow.node.knowledge.node import KnowledgeNodeDatasetConfig
from app.core.workflow.node_variable.base import VariableType, InputType
from app.core.workflow.state import GraphState
from app.logger import logger
from app.models.rag.dataset import Dataset


@pytest.fixture
def graph_json():
    id_length = 8
    start_node_id = NodeType.START.value
    knowledge_node_id = NodeType.KNOWLEDGE.value + "_" + str(uuid.uuid4())[:id_length]
    plugin_node_id = NodeType.PLUGIN.value + "_" + str(uuid.uuid4())[:id_length]
    end_node_id = NodeType.END.value

    return {
        "nodes": [
            {
                "id": start_node_id,
                "name": NodeType.START.name,
                "node_type": NodeType.START.value,
                "inputs": [
                    {
                        "name": "BOT_USER_INPUT",
                        "variable_type": VariableType.STRING.value,
                        "value": "Hello, 请问创业该懂那些?",
                        "is_editable": False,
                    },
                    {
                        "name": "company_name",
                        "variable_type": VariableType.STRING.value,
                        "value": "公司在上海?",
                    },
                ],
            },
            {
                "id": knowledge_node_id,
                "name": NodeType.KNOWLEDGE.name,
                "node_type": NodeType.KNOWLEDGE.value,
                "datasets": [
                    Dataset.create_dataset(name="test_dataset_1"),  # 修改这里
                    Dataset.create_dataset(name="test_dataset_2"),  # 修改这里
                ],
                "config": KnowledgeNodeDatasetConfig(),
                "inputs": [
                    {
                        "name": "company_name_start",
                        "input_type": InputType.REFERENCE.value,
                        "variable_type": VariableType.STRING.value,
                        "reference_var": {
                            start_node_id: start_node_id + "." + "company_name"
                        },
                    },
                ],
            },
            {
                "id": plugin_node_id,
                "name": NodeType.PLUGIN.name,
                "node_type": NodeType.PLUGIN.value,
                "tools": [],
                "inputs": [
                    {
                        "name": "company_name_start_2",
                        "input_type": InputType.REFERENCE.value,
                        "variable_type": VariableType.STRING.value,
                        "reference_var": {
                            start_node_id: start_node_id + "." + "company_name"
                        },
                    },
                    {
                        "name": "company_name_plugin",
                        "input_type": InputType.REFERENCE.value,
                        "variable_type": VariableType.STRING.value,
                        "reference_var": {
                            start_node_id: plugin_node_id + "." + "company_1_name"
                        },
                    },
                ],
            },
            {
                "id": end_node_id,
                "name": NodeType.END.name,
                "node_type": NodeType.END.value,
                "inputs": [
                    {
                        "name": "company_name_start_3",
                        "input_type": InputType.REFERENCE.value,
                        "variable_type": VariableType.STRING.value,
                        "reference_var": {
                            start_node_id: start_node_id + "." + "company_name"
                        },
                    },
                    {
                        "name": "company_name_knowledge_1",
                        "input_type": InputType.REFERENCE.value,
                        "variable_type": VariableType.STRING.value,
                        "reference_var": {
                            start_node_id: start_node_id + "." + "company_1_name"
                        },
                    },
                ],
            },
        ],
        "edges": [
            {
                "source": start_node_id,
                "target": knowledge_node_id,
                "edge_type": "single",
            },
            {
                "source": knowledge_node_id,
                "target": plugin_node_id,
                "edge_type": "single",
            },
            {"source": plugin_node_id, "target": end_node_id, "edge_type": "single"},
        ],
    }


def test_graph_run(graph_json):
    try:
        graph = create_graph_from_json(graph_json)

        assert graph is not None

        graph.run(GraphState(question="1+1*3/2=?", messages=[]))
    except Exception as e:
        logger.error(e, exc_info=settings.log.exc_info)
        pytest.fail(f"Test failed with exception: {e}")
