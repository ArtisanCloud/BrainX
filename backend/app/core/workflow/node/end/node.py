from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import add_messages

from app.core.workflow.node.base import BaseNode
from app.core.workflow.state import GraphState


class EndNode(BaseNode):
    def __init__(self, node_data: dict):
        super().__init__(node_data)

    def execute(self, state: GraphState):
        super().execute(state)

        # node_list = self.context_manager.get_node_list()
        print(f"---"
              # f"dataset: {self.datasets}, "
              # f"node_list: {node_list}"
              f"inputs: {self.input_vars}"
              f"---")

        from langchain.prompts import PromptTemplate

        template = """你是一个用于回答问题任务的助手。使用以下检索到的内容来回答问题。如果你不知道答案，只需说明不知道。回答最多使用三句话，并保持简洁。

        问题：{question}

        上下文：{context}

        回答：
        """

        prompt = PromptTemplate(
            input_variables=["question", "context"],
            template=template,
        )

        rag_chain = prompt | self.llm | StrOutputParser()

        response = rag_chain.invoke({"context": state["messages"], "question": state["question"]})
        print(22222, response)
        return {"messages": [response]}
