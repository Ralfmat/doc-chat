import asyncio
import logging
import fitz  # PyMuPDF
from app.core.celery_app import celery_app

logger = logging.getLogger(__name__)

async def extract_text_from_pdf(file_path: str) -> str:
    """
    Async function to extract text from a PDF file using PyMuPDF (fitz).
    In future I'll use langchain's PDF loader, but for now this serves as a simple proof of concept.
    """
    logger.info(f"Extracting text from PDF: {file_path}")
    text = ""
    
    try:
        doc = fitz.open(file_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
        doc.close()
        
        logger.info(f"Success! Extracted {len(text)} characters from {file_path}.")
        
        # Na potrzeby Fazy 3: logujemy początek wyciągniętego tekstu do konsoli
        print(f"\n Extracted ({file_path})")
        print(text[:500] + "...\n[Rest of the text truncated for readability]\n")
        
        return text
    except Exception as e:
        logger.error(f"Error parsing PDF {file_path}: {e}")
        raise e

@celery_app.task(bind=True, max_retries=3)
def process_pdf_task(self, file_path: str, document_id: str):
    """
    Celery task to process a PDF file and extract its text content.
    """
    try:
        
        result_text = asyncio.run(extract_text_from_pdf(file_path))
        
        return {
            "status": "SUCCESS", 
            "document_id": document_id, 
            "extracted_length": len(result_text)
        }
    except Exception as exc:
        logger.warning(f"Task failed, retrying... ({exc})")
        # Retry in case of failure, with a delay of 5 seconds between retries
        raise self.retry(exc=exc, countdown=5)