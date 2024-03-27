from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Union, Any
from uuid import UUID
from datetime import datetime

class Base(BaseModel):
    id: Optional[UUID] = Field(None, description="Unique identifier")
    created_at: Optional[datetime] = Field(None, description="Creation datetime")
    updated_at: Optional[datetime] = Field(None, description="Update datetime")

    class Config:
        from_attributes = True


class BaseMetadataObject(BaseModel):
    class Config:
        from_attributes = True

