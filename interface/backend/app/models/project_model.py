from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from beanie import Document, Indexed, Link, before_event, Replace, Insert
from pydantic import Field
from app.models.user_model import User

class Project(Document):
    project_id: UUID = Field(default_factory=uuid4, unique=True)
    description: Optional[str] = Field(..., title="Description", min_length=3, max_length=500)
    title: Indexed(str)
    status: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    owner: Link[User]

    def __repr__(self):
        return f"<Project {self.title}>"
    
    def __str__(self):
        return self.title
    
    def __hash__(self) -> int:
        return hash(self.title)
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Project):
            return self.project_id == other.project_id
        return False

    @before_event([Replace, Insert])
    async def update_updated_at(self):
        self.updated_at = datetime.utcnow()
    
    class Settings:
        name = "projects"