from fastapi import FastAPI
from app.api.endpoints import documents

app = FastAPI(
    title="DocChat API",
    description="Async ETL pipeline and RAG architecture for processing PDFs.",
    version="1.0.0",
)

app.include_router(documents.router, prefix="/documents", tags=["Documents"])

@app.get("/health")
async def health_check():
    """Simple health check endpoint to verify the API is running."""
    return {"status": "ok", "message": "DocChat API is active."}