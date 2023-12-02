from fastapi import HTTPException, status
import requests
from app.core.config import settings


class CamundaService:
    @staticmethod
    async def Start_process(content, project):
        try:
            if content is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")

            json = {
                    "variables": {
                        "project_id": {
                            "value": str(project.id),
                            "type": "String"
                        },
                        "accession_id": {
                            "value": content.accession_id,
                            "type": "String"
                        },
                        "clinic_id": {
                            "value": content.clinic_id,
                            "type": "String"
                        },
                        "modalities": {
                            "value": content.modalities,
                            "type": "String" 
                        },
                        "date": {
                            "value": content.date,
                            "type": "String"
                        },
                        "series_id": {
                            "value": content.series_id,
                            "type": "String"
                        },
                        "study_id": {
                            "value": content.study_id,
                            "type": "String"
                        },
                    }
                }
            
            response = requests.post(
                url=f'{settings.CAMUNDA_REST_URL}{settings.CAMUNDA_WORKFLOW_ID}/start',
                headers= {'Content-Type': 'application/json'},
                json=json
            )
            
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    