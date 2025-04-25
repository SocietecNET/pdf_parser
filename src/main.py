from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool
from .utils.extract_content import extract_content
import base64
import io
import pypdfium2


class PdfRequest(BaseModel):
    pdf_base64: str
    page_from: Optional[int] = None
    page_to: Optional[int] = None


app = FastAPI()


def process_pdf(pdf_bytes, page_from, page_to):
    # Create PDF from bytes
    pdf = pypdfium2.PdfDocument(pdf_bytes)
    
    # Select pages (0-indexed)
    start = page_from - 1 if page_from else 0
    end = page_to if page_to else len(pdf)
    pages = range(start, end)
    
    # Create new PDF with selected pages
    new_pdf = pypdfium2.PdfDocument.new()
    for i in pages:
        new_pdf.import_pages(pdf, [i])
    
    # Save to memory buffer
    buffer = io.BytesIO()
    new_pdf.save(buffer)
    buffer.seek(0)
    
    # Process the PDF
    return extract_content(buffer)


@app.get("/health")
async def health_check():
    return {"status": "OK"}


@app.post("/convert")
async def convert(request: PdfRequest):
    pdf_bytes = base64.b64decode(request.pdf_base64)
    pages = await run_in_threadpool(
        process_pdf, pdf_bytes, request.page_from, request.page_to
    )
    return {"pages": pages}
