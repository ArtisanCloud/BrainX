# from app.core.rag.synthesis.drivers.langchain.executor import LangchainAgentExecutor
# from app.core.rag.synthesis.interface import BaseAgentExecutor
#
#
# class AgentExecutorFactory:
#
#     @staticmethod
#     def get_agent_executor(
#             llm: str,
#             temperature: float = 0.5,
#             streaming: bool = False,
#     ) -> BaseAgentExecutor:
#         return LangchainAgentExecutor(
#             llm=llm,
#             temperature=temperature,
#             streaming=streaming
#         )
