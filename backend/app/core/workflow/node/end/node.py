from langchain_core.output_parsers import StrOutputParser

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

        default_persona = "你是一个用于回答问题任务的助手。如果有上下文，请按照上下文回答问题。如果你不知道答案，只需说明不知道。"
        # 如果app存在，则使用app的persona
        if self.app:
            default_persona = "你是一个用于回答问题任务的助手。使用以下检索到的内容来回答问题。如果你不知道答案，只需说明不知道。回答最多使用三句话，并保持简洁。"
            persona = self.app.persona if self.app.persona else default_persona
        else:
            persona = default_persona
        template_structure = """

        问题：{question}

        上下文：{context}

        要求: 如果有阐述回答内容，尽量有条有理的回答，分析和总结部分 
        
        回答：
        """
        template = persona + template_structure

        prompt = PromptTemplate(
            input_variables=["question", "context"],
            template=template,
        )

        rag_chain = prompt | self.llm | StrOutputParser()

        # print(1111111, state["messages"])
        response = rag_chain.stream({"context": state["messages"], "question": state["question"]})
        print(22222, response)
        return {
            "result": response,
            # "messages": [response]
        }
