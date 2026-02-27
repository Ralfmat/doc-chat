from pydantic import BaseModel, Field

class UploadResponse(BaseModel):
    filename: str
    task_id: str
    message: str

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    # it will be expanded later