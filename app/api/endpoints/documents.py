import os
import uuid
import aiofiles
from app.models.document import Document
from app.api.dependencies import get_db
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from app.schemas.document import UploadResponse, TaskStatusResponse
from sqlalchemy.ext.asyncio import AsyncSession

# Right now I use local file storage for simplicity, but I'm going to switch to S3

router = APIRouter(prefix="/api/v1/documents", tags=["Documents"])

UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_document(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    """Receives a PDF, saves it asynchronously, and triggers a background extraction task."""
    
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    
    # async file saving prevents blocking the FastAPI event loop
    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            while content := await file.read(1024 * 1024): 
                await out_file.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
        
    # TODO replace this mock UUID with actual `task = process_pdf.delay(file_path)`
    mock_task_id = str(uuid.uuid4())
    
    new_document = Document(
        filename=file.filename,
        task_id=mock_task_id,
        status="PENDING"
    )
    db.add(new_document)
    await db.commit()
    await db.refresh(new_document)

    return UploadResponse(
        filename=file.filename,
        task_id=mock_task_id,
        message="File uploaded successfully. Background processing initiated."
    )

@router.get("/status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """Checks the status of a Celery background task."""
    # TODO query actual Celery AsyncResult(task_id)
    return TaskStatusResponse(
        task_id=task_id,
        status="PENDING" 
    )