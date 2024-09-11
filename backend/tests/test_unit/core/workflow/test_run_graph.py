import uuid
import pytest

from app import settings
from app.core.workflow.graph import create_graph_from_json
from app.core.workflow.node.base import NodeType
from app.core.workflow.node_variable.base import VariableType, InputType
from app.core.workflow.state import GraphState
from app.logger import logger


@pytest.fixture
def graph_json():
    id_length = 8
    start_node_id = NodeType.START.id
    knowledge_node_id = NodeType.KNOWLEDGE.id + "_" + str(uuid.uuid4())[:id_length]
    plugin_node_id = NodeType.PLUGIN.id + "_" + str(uuid.uuid4())[:id_length]
    end_node_id = NodeType.END.id

    return {
        "nodes": [
            {
                "id": start_node_id, "name": NodeType.START.name, "node_type": NodeType.START.type,
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
                        "value": "公司在上海?"
                    }
                ]
            },
            {
                "id": knowledge_node_id, "name": NodeType.KNOWLEDGE.name, "node_type": NodeType.KNOWLEDGE.type,
                "datasets": [
                    {
                        "dataset_uuid": "dataset_uuid_1",
                    },
                    {
                        "dataset_uuid": "dataset_uuid_2",
                    },
                ],
                "inputs": [
                    {
                        "name": "company_name_start",
                        "input_type": InputType.REFERENCE.value,
                        "variable_type": VariableType.STRING.value,
                        "reference_var": {
                            start_node_id: start_node_id + "." + "company_name"
                        },
                    },
                ]
            },
            {
                "id": plugin_node_id, "name": NodeType.PLUGIN.name, "node_type": NodeType.PLUGIN.type,
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
                ]
            },
            {
                "id": end_node_id, "name": NodeType.END.name, "node_type": NodeType.END.type,
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
                ]
            }
        ],
        "edges": [
            {"source": start_node_id, "target": knowledge_node_id, "edge_type": "single"},
            {"source": knowledge_node_id, "target": plugin_node_id, "edge_type": "single"},
            {"source": plugin_node_id, "target": end_node_id, "edge_type": "single"}
        ]
    }


def test_graph_run(graph_json):
    try:
        graph = create_graph_from_json(graph_json)

        assert graph is not None

        graph.run(
            GraphState(messages=["1+1*3/2=?"])
        )
    except Exception as e:
        logger.error(e, exc_info=settings.log.exc_info)
        pytest.fail(f"Test failed with exception: {e}")
