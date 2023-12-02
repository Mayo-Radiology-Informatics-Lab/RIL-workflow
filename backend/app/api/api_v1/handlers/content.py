from fastapi import APIRouter, Depends, File, UploadFile
from app.models.user_model import User
from app.models.project_model import Project
from app.api.deps.user_deps import get_current_user
from app.api.deps.project_deps import get_current_project
from app.schemas.content_schema import ContentCreate, ContentUpdate, ContentOut
from app.services.content_service import ContentService
from uuid import UUID
from typing import List



content_router = APIRouter()

@content_router.get("/{project_id}", summary="Get all contents of a user", response_model= List[ContentOut])
async def List(current_project: Project = Depends(get_current_project),
               current_user: User = Depends(get_current_user)
            ):
    return await ContentService.List_contents(current_project, current_user)



@content_router.post("/{project_id}/create", summary="Create a content", response_model=ContentOut)
async def Create_content(data: ContentCreate,
                        current_project: Project = Depends(get_current_project),
                        current_user: User = Depends(get_current_user)
                    ):
    return await ContentService.Create_content(data, current_project, current_user)



@content_router.get("/{project_id}/{content_id}", summary="Get a content by content_id", response_model=ContentOut)
async def Get_content(content_id: UUID,
                        current_project: Project = Depends(get_current_project),
                        current_user: User = Depends(get_current_user)
                    ):
    return await ContentService.Get_content(content_id, current_project, current_user)



@content_router.put("/{project_id}/{content_id}", summary="Update a content by content_id", response_model=ContentOut)
async def Update_content(content_id: UUID, data: ContentUpdate,
                        current_project: Project = Depends(get_current_project),
                        current_user: User = Depends(get_current_user)
                    ):
    return await ContentService.Update_content(content_id, data, current_project, current_user)



@content_router.delete("/{project_id}/{content_id}", summary="Delete a content by content_id")
async def Delete_content(content_id: UUID,
                        current_project: Project = Depends(get_current_project),
                        current_user: User = Depends(get_current_user)
                    ):
    await ContentService.Delete_content(content_id, current_project, current_user)
    return None



@content_router.post("/{project_id}/upload", summary="Upload a file to create contents")
async def Upload_file(file: UploadFile = File(...),
                        current_project: Project = Depends(get_current_project),
                        current_user: User = Depends(get_current_user)
                    ):
    return await ContentService.create_content_by_file(file, current_project, current_user)