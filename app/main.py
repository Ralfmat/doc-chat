from fastapi import FastAPI

app = FastAPI(
    title="DocChat API",
    description="Async ETL pipeline and RAG architecture for processing PDFs.",
    version="1.0.0",
)

@app.get("/health")
async def health_check():
    """Simple health check endpoint to verify the API is running."""
    return {"status": "ok", "message": "DocChat API is active."}