import http
from typing import List

from app import settings
from app.logger import logger
from app.models.rag.document_node import DocumentNode
from app.schemas.base import ResponseSchema
from app.schemas.question_answer.query import ResponseQuery, Document as DocumentSchema
from app.service.brainx import BrainXService


def transform_documents_to_reply(answer: str, documents: List[DocumentNode]) -> ResponseQuery:
    return ResponseQuery(
        answer=answer,
        documents=[
            transform_document_to_reply(document)
            if document is not None
            else None
            for document in documents
        ]
    )


def transform_document_to_reply(document: DocumentNode) -> DocumentSchema:
    return DocumentSchema(
        # text=document.page_content,
        text="",
        similarity=document.metadata.get("score", 0.0),
        node_id=document.metadata['node_id'],
        metadata=document.metadata,
    )


async def query_by_text(
        question: str,
        llm: str
) -> ResponseQuery | ResponseSchema:
    service_brain_x = BrainXService(
        llm,
        streaming=False,
        collection_name="opl_embeddings"
    )

    res = ResponseQuery(answer="暂时没有找到答案，请稍后再试。", documents=[])
    try:
        # retrieve langchain documents
        docs, exception = await service_brain_x.retrieve(
            question,
            top_k=2,
            score_threshold=0.7
        )
        # print(docs)

        if exception:
            raise exception

        if len(docs) > 0:
            template = (docs[0].page_content +
                        " \n\n 请根据以上召回内容，针对此问题'{query}'，做一个回答")
            # print(template)
            response, exception = service_brain_x.complete(
                query=question,
                input_variables=["query"],
                template=template
            )
            if exception:
                raise exception

            # print(response)
            # for ollama response
            if isinstance(response, str):
                return transform_documents_to_reply(response, docs)

            res = transform_documents_to_reply(response.content, docs)

    except Exception as e:
        logger.info(f"Error in query_by_text: {e}", exc_info=settings.log.exc_info)
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    # logger.info(repr(response))
    # logger.info(response.source_nodes[0].score)
    # print(docs)

    return res
