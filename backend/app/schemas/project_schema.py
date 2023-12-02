from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class ProjectCreate(BaseModel):
    title: str = Field(..., title="Title", min_length=3, max_length=50)
    description: str = Field(..., title="Description", min_length=3, max_length=500)
    status: bool = True

class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(..., title="Title", min_length=3, max_length=50)
    description: Optional[str] = Field(..., title="Description", min_length=3, max_length=500)
    status: bool = True

class ProjectOut(BaseModel):
    project_id: UUID
    title: str = Field(..., title="Title", min_length=3, max_length=50)
    description: str = Field(..., title="Description", min_length=3, max_length=500)
    status: bool = True
    created_at: datetime
    updated_at: datetime