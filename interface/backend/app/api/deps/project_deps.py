from uuid import UUID
from app.api.deps.user_deps import get_current_user
from fastapi import Depends, HTTPException, status, Request
from app.models.user_model import User
from app.models.project_model import Project
from app.services.project_service import ProjectService


async def get_current_project(project_id: UUID, current_user: User = Depends(get_current_user)) -> Project:

    project = await ProjectService.Get_project(project_id, current_user)

    if not project:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    return project