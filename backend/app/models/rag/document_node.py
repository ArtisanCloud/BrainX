from pydantic import BaseModel
from typing import Optional, Dict, Any, List


class DocumentNode(BaseModel):
    page_content: str
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self):
        return {
            "page_content": self.page_content,
            "metadata": self.metadata,
        }