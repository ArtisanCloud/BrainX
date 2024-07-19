from typing import List, Optional

from app.models import Document


class Dataset:
    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description
        self.documents: List[Document] = []

    def add_document(self, document: Document):
        """添加一个文档到数据集中"""
        self.documents.append(document)

    def remove_document(self, document: Document):
        """从数据集中移除一个文档"""
        if document in self.documents:
            self.documents.remove(document)

    def clear_documents(self):
        """清空数据集中的所有文档"""
        self.documents.clear()

    def get_document_by_id(self, doc_id: str) -> Optional[Document]:
        """通过文档ID获取文档"""
        for doc in self.documents:
            if doc.id == doc_id:
                return doc
        return None

    def get_document_count(self) -> int:
        """获取数据集中文档的数量"""
        return len(self.documents)

    def __str__(self):
        return f"Dataset: {self.name}, Document count: {len(self.documents)}"
