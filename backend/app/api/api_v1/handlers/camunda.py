from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user_model import User
from app.models.project_model import Project
from app.api.deps.user_deps import get_current_user
from app.api.deps.project_deps import get_current_project
from app.services.camunda_services import CamundaService
from uuid import UUID



camunda_router = APIRouter()

# send a json file by content_id to camunda server
@camunda_router.post("/{content_id}", summary="Send a content by content_id")
async def send_camunda(content_id: UUID,
                        current_project: Project = Depends(get_current_project),
                        current_user: User = Depends(get_current_user)
                    ):
    return await CamundaService.send_camunda(content_id, current_project, current_user)
    