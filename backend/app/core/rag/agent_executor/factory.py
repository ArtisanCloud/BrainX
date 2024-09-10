from app.core.rag import FrameworkDriverType
from app.core.rag.agent_executor.drivers.langchain.executor import LangchainAgentExecutor
from app.core.rag.agent_executor.drivers.llamaindex.executor import LlamaIndexAgentExecutor
from app.core.rag.agent_executor.interface import BaseAgentExecutor


class AgentExecutorFactory:

    @staticmethod
    def get_agent_executor(
            framework_type: FrameworkDriverType,
            llm: str,
            temperature: float = 0.5,
            streaming: bool = False,
    ) -> BaseAgentExecutor:
        match framework_type.value:
            # LlamaIndex are supported
            case FrameworkDriverType.LLAMA_INDEX.value:
                return LlamaIndexAgentExecutor(
                    llm=llm,
                    temperature=temperature,
                    streaming=streaming
                )

            # Langchain are supported
            case FrameworkDriverType.LANGCHAIN.value:
                return LangchainAgentExecutor(
                    llm=llm,
                    temperature=temperature,
                    streaming=streaming
                )

            # Other types are not supported
            case _:
                raise ValueError(f"Unknown agent_executor type: {framework_type}")
