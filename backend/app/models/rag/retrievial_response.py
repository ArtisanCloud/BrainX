from pydantic import BaseModel
from typing import Optional, Dict, Any, List


class RetrievalResponse(BaseModel):
    id: str
    content: str
    additional_kwargs: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "additional_kwargs": self.additional_kwargs,
            "metadata": self.metadata,
        }