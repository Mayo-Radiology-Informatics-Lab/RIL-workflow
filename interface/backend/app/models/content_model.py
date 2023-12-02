from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from beanie import Document, Indexed, Link, before_event, Replace, Insert
from pydantic import Field
from app.models.user_model import User
from app.models.project_model import Project


class Content(Document):
    content_id: Indexed(UUID) = Field(default_factory=uuid4, unique=True)
    accession_id: Optional[str] = Field(..., default_factory=None, title="Accession Number", min_length=3, max_length=500, unique=True)
    clinic_id: Optional[str] = Field(..., default_factory=None, title="Clinic ID", min_length=3, max_length=500)
    report_id: Optional[str] = Field(..., default_factory=None, title="Report ID", min_length=3, max_length=500)
    date: Optional[str] = Field(..., default_factory=None, title="Exam Date", min_length=3, max_length=500)
    series_id: Optional[str] = Field(..., default_factory=None, title="Series ID", min_length=3, max_length=500)
    study_id: Optional[str] = Field(..., default_factory=None, title="Study ID", min_length=3, max_length=500)
    modalities: Optional[str] = Field(..., default_factory=None, title="Type of Modality", min_length=3, max_length=500)
    other_content: Optional[object]
    status: Optional[bool] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    owner: Link[User]
    project: Link[Project]

    def __repr__(self):
        return f"<Content {self.content_id}>"
    
    def __str__(self):
        return self.content_id
    
    def __hash__(self) -> int:
        return hash(self.content_id)
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Content):
            return self.content_id == other.content_id
        return False

    @before_event([Replace, Insert])
    async def update_updated_at(self):
        self.updated_at = datetime.utcnow()
    
    class Settings:
        name = "contents"