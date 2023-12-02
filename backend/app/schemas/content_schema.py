from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

class ContentCreate(BaseModel):
    accession_id: Optional[str] = Field(..., default_factory=None, title="Accession Number", min_length=3, max_length=500, unique=True)
    clinic_id: Optional[str] = Field(..., default_factory=None, title="Clinic ID", min_length=3, max_length=500)
    report_id: Optional[str] = Field(..., default_factory=None, title="Report ID", min_length=3, max_length=500)
    date: Optional[str] = Field(..., default_factory=None, title="Exam Date", min_length=3, max_length=500)
    series_id: Optional[str] = Field(..., default_factory=None, title="Series ID", min_length=3, max_length=500)
    study_id: Optional[str] = Field(..., default_factory=None, title="Study ID", min_length=3, max_length=500)
    modalities: Optional[str] = Field(..., default_factory=None, title="Type of Modality", min_length=3, max_length=500)
    other_content: Optional[object]
    status: Optional[bool] = None

class ContentUpdate(BaseModel):
    accession_id: Optional[str]
    clinic_id: Optional[str]
    report_id: Optional[str]
    date: Optional[str]
    series_id: Optional[str]
    study_id: Optional[str]
    modalities: Optional[str]
    other_content: Optional[object]
    status: Optional[bool]

class ContentOut(BaseModel):
    content_id: UUID
    accession_id: Optional[str] = Field(..., default_factory=None, title="Accession Number", min_length=3, max_length=500, unique=True)
    clinic_id: Optional[str] = Field(..., default_factory=None, title="Clinic ID", min_length=3, max_length=500)
    report_id: Optional[str] = Field(..., default_factory=None, title="Report ID", min_length=3, max_length=500)
    date: Optional[str] = Field(..., default_factory=None, title="Exam Date", min_length=3, max_length=500)
    series_id: Optional[str] = Field(..., default_factory=None, title="Series ID", min_length=3, max_length=500)
    study_id: Optional[str] = Field(..., default_factory=None, title="Study ID", min_length=3, max_length=500)
    modalities: Optional[str] = Field(..., default_factory=None, title="Type of Modality", min_length=3, max_length=500)
    other_content: Optional[object]
    status: Optional[bool]
    created_at: datetime
    updated_at: datetime