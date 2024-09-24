from pydantic import BaseModel
from typing import Optional, Dict, Any, List


class InvokeResponse(BaseModel):
    id: Optional[str] = None
    content: Optional[str] = None
    type: Optional[str] = None
    name: Optional[str] = None
    additional_kwargs: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "type": self.type,
            "name": self.name,
            "additional_kwargs": self.additional_kwargs,
            "metadata": self.metadata,
        }