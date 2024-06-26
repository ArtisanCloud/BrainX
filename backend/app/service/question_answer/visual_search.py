import json

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.question_answer.question_answer import table_name_text_embedding, table_name_image_embedding
from app.schemas.question_answer.visual_search import ResponseVisualSearch
from app.schemas.question_answer.query import Document as DocumentSchema
from app.schemas.question_answer.visual_search import ImageDocument as ImageDocumentSchema


def transform_image_documents_to_reply(documents: [any]) -> ResponseVisualSearch:
    return ResponseVisualSearch(
        image_documents=[transform_image_document_to_reply(document) for document in documents]
    )


def transform_image_document_to_reply(document: any) -> ImageDocumentSchema:
    return ImageDocumentSchema(
        image=document.image,
        question=document.question,
        relative_document=DocumentSchema(
            similarity=document.similarity,
            text=document.text,
            node_id=document.node_id,
            metadata=document.metadata,
        ),
    )


async def visual_search(
        db: AsyncSession,
        target_embedding: any,
        match_threshold=0.5,
) -> ResponseVisualSearch | None:
    # print(db)
    # print(question)

    target_embedding_json = json.dumps(target_embedding)

    query = text("""
                SELECT 
                    ie.image as image,
                    ie.question as question,
                    te.text as text,
                    te.node_id as node_id,
                    te.metadata_ as metadata, 
                    (ie.embedding <=> :target_embedding) AS similarity
                FROM data_image_embeddings ie
                LEFT JOIN 
                data_embeddings te ON ie.doc_id = te.id
                WHERE (ie.embedding <=> :target_embedding) < :match_threshold
                ORDER BY similarity ASC
                LIMIT 3;
            """)
    params = {
        "target_embedding": target_embedding_json,
        "match_threshold": match_threshold,
        "data_embeddings": table_name_text_embedding,
        "data_image_embeddings": table_name_image_embedding
    }
    result = await db.execute(query, params)
    rows = result.mappings().all()

    # logger.info(rows)

    res = transform_image_documents_to_reply(rows)

    return res
