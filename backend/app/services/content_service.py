from typing import List
from fastapi import File, HTTPException, status
from app.models.user_model import User
from app.models.project_model import Project
from app.models.content_model import Content
from app.schemas.content_schema import ContentCreate, ContentUpdate
from app.services.camunda_services import CamundaService
from uuid import UUID
import shutil, os
from datetime import datetime
import pandas as pd
import requests

class ContentService:
    @staticmethod
    async def List_contents(project: Project, user: User) -> List[Content]:
        contents = await Content.find(Content.project.id == project.id, Content.owner.id == user.id).to_list()
        return contents

    @staticmethod
    async def Create_content(data: ContentCreate, project: Project, user: User) -> Content:
        content = Content(**data.dict(), project=project, owner=user)
        
        if content.accession_id:
            is_content = await Content.find_one(Content.accession_id == content.accession_id, Content.project.id == project.id)
        elif content.clinic_id:
            is_content = await Content.find_one(Content.clinic_id == content.clinic_id, Content.project.id == project.id)
        
        if is_content:
            return await ContentService.Update_content(is_content.content_id, data, project, user)
        else:
            return await content.insert()

    @staticmethod
    async def Get_content(content_id: UUID, project: Project, user: User):
        content = await Content.find_one(
            Content.content_id == content_id, Content.project.id == project.id, Content.owner.id == user.id
        )
        return content

    @staticmethod
    async def Update_content(content_id: UUID, data: ContentUpdate, project: Project, user: User):
        content = await ContentService.Get_content(content_id, project, user)
        await content.update({"$set": data.dict(exclude_unset=True)})
        await content.save()
        if data.status == True:
            await CamundaService.Start_process(content, project)
        return content

    @staticmethod
    async def Delete_content(content_id: UUID, project: Project, user: User) -> List[Content]:
        content = await ContentService.Get_project(content_id, project, user)
        if content:
            await content.delete()
        return None

    @staticmethod
    async def create_content_by_file(file: File(...), project: Project, user: User):
    # Uploading the file to the server
        try:
            # Checking if the file is in the correct format
            file_extension = os.path.splitext(file.filename)[-1]
            if file_extension not in ['.csv', '.xlsx', '.xls']:
                return {"message": "The file should be in Excel or CSV format.", "code": 500}
            
            # Saving the file to disk
            file_path = os.path.join(os.getcwd(), 'app', 'uploads', f"{user.username}_{(project.title).replace('/','')}_{datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S')}{file_extension}")
            with open(file_path, 'wb') as buffer:
                shutil.copyfileobj(file.file, buffer)
                
            # Create a data frame from the file
            if file_extension == '.csv':
                df = pd.read_csv(file_path, header=0)
            elif file_extension in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path, header=0)

            # Converting the data frame to a list of dictionaries
            for index, row in df.iterrows():
                content = ContentCreate(
                    accession_id = None,
                    clinic_id = None,
                    report_id = None,
                    report_date = None,
                    modalities = None,
                    other_content = None,
                )
                other_content = [{}]
                for key, value in row.items():
                    key = key.lower()
                    if 'accession' in key:
                        content.accession_id = str(value)
                    elif 'clinic' in key or 'patient' in key:
                        content.clinic_id = str(value)
                    elif 'report' in key and 'id' in key:
                        content.report_id = str(value)
                    elif 'date' in key:
                        content.report_date = str(value)
                    elif 'modality' in key:
                        content.modalities = str(value)
                    else:
                        other_content[0][key] = str(value)
                content.other_content = other_content
                # Create the content
                await ContentService.Create_content(content, project, user)
                
            # Deleting the file from the server
            #os.remove(file_path)

            # Return a success message
            return {"message": f"Successfully uploaded {file.filename} and created contents.", "code": 200}

        except Exception as e:
            print("err {e}")
            return {"message": f"Error uploading file {file.filename}: {e}.", "code": 500}
    