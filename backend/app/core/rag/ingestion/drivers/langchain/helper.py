import uuid
from typing import List, Tuple

from langchain_core.documents import Document
from langchain_core.runnables.utils import Output

from app.core.libs.node import generate_node_hash
from app.models.rag.document_node import DocumentNode
from app.models.rag.invoke_response import InvokeResponse


def convert_node_to_document(node: DocumentNode) -> Document:
    return Document(
        page_content=node.page_content,
        metadata=node.metadata
    )


def convert_nodes_to_documents(nodes: List[DocumentNode]) -> List[Document]:
    return [
        convert_node_to_document(node)
        for node in nodes
    ]


def convert_document_to_node(document: Document) -> DocumentNode:
    return DocumentNode(
        page_content=document.page_content,
        metadata={
            **document.metadata,
            "node_id": document.metadata["node_id"] if "node_id" in document.metadata else str(uuid.uuid4()),
            "node_hash": generate_node_hash(document.page_content)
        }
    )


def convert_documents_to_nodes(documents: List[Document]) -> List[DocumentNode]:
    return [
        convert_document_to_node(document)
        for document in documents
    ]


def convert_document_to_nodes_with_score(doc: Tuple[Document, float]) -> DocumentNode:
    document, score = doc

    node = convert_document_to_node(document)

    node.metadata["score"] = score
    return node


def convert_documents_to_nodes_with_score(documents: List[Document | Tuple[Document, float]]) -> List[DocumentNode]:
    return [
        convert_document_to_nodes_with_score(document)
        for document in documents
    ]


def convert_document_to_response(output: Output) -> InvokeResponse:
    return InvokeResponse(
        id=output.id,
        name=output.name,
        type=output.type,
        content=output.content,
        additional_kwargs=output.additional_kwargs,
        metadata=output.response_metadata,
    )
