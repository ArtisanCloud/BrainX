import pytest
import logging

from app.core.agent_bot.agent import AgentBot, create_graph_from_json
from app.core.workflow.state import GraphState
from app.models import AppModelConfig


@pytest.fixture
def setup_agent_bot():
    """Fixture to set up the AgentBot instance."""
    return AgentBot(None, AppModelConfig(
        persona_prompt="""
        # Character
        You are an expert at routing a user question to a vectorstore or web search.

        ## Skills
        The vectorstore contains documents related to agents, prompt engineering, and adversarial attacks.
        1. Use the vectorstore_retrieve for questions on these topics. 
        2. 使用web_search来互联网上网问题 ；
        3. 使用local_tool来处理本地系统文件复制操作； 
        """,
        app_uuid="app_uuid_111",
        model_provider_uuid="model_provider_uuid_111",
    ))


def test_agent_bot_run(setup_agent_bot):
    """Test the AgentBot run method."""

    try:
        agent_bot = setup_agent_bot
        assert agent_bot is not None

        state = GraphState(
            question="RAG里的Agent有多少种类型？",
            messages=[""]
        )
        # Assuming `run` method returns some output or has side effects to test
        agent_bot.run(state)

    except Exception as e:
        logger.error(e, exc_info=settings.log.exc_info)
        pytest.fail(f"Test failed with exception: {e}")

