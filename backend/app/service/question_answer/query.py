import http
from typing import List

from langchain_core.documents import Document

from app.logger import logger
from app.schemas.base import ResponseSchema
from app.schemas.question_answer.query import ResponseQuery, Document as DocumentSchema
from app.service.brainx import BrainXService


def transform_documents_to_reply(answer: str, documents: List[Document]) -> ResponseQuery:
    return ResponseQuery(
        answer=answer,
        documents=[
            transform_document_to_reply(document)
            if document is not None
            else None
            for document in documents
        ]
    )


def transform_document_to_reply(document: Document) -> DocumentSchema:

    return DocumentSchema(
        text=document.page_content,
        similarity=document.metadata['score'],
        node_id=document.metadata['node_id'],
        metadata=document.metadata['metadata'],
    )


async def query_by_text(
        question: str,
        llm: str
) -> ResponseQuery | ResponseSchema:

    service_brain_x = BrainXService(llm, 1, False)

    try:
        # retrieve langchain documents
        docs = await service_brain_x.retrieve(question, 1)
        # print(docs)
        template = (docs[0][0].page_content +
                    " \n\n 请根据以上的问答信息，用中文来回答这个问题：{query}")
        # print(template)

        response, exception = service_brain_x.complete(
            inputs={"query": question},
            input_variables=["query"],
            template=template
        )
        if exception:
            raise exception

        # print(response,docs)
        # for ollama response
        if isinstance(response, str):
            return transform_documents_to_reply(response, docs[0])

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    # logger.info(repr(response))
    # logger.info(response.source_nodes[0].score)
    # print(docs)

    res = transform_documents_to_reply(response.content, docs[0])

    return res
