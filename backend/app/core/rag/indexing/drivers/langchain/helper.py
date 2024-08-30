import uuid
from typing import List

from langchain_core.documents import Document

from app.core.libs.node import generate_node_hash
from app.models.rag.document_node import DocumentNode


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
            "node_id": str(uuid.uuid4()),
            "node_hash": generate_node_hash(document.page_content)
        }
    )


def convert_documents_to_nodes(documents: List[Document]) -> List[DocumentNode]:
    return [
        convert_document_to_node(document)
        for document in documents
    ]
