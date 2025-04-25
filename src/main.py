from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from .utils.extract_content import extract_content
import base64
import io


class PdfRequest(BaseModel):
    pdf_base64: str
    page_from: Optional[int] = None
    page_to: Optional[int] = None


app = FastAPI()


@app.get("/health")
async def health_check():
    return {"status": "OK"}


@app.post("/convert")
async def convert(request: PdfRequest):
    pdf_bytes = base64.b64decode(request.pdf_base64)
    pdf_file = io.BytesIO(pdf_bytes)

    all_pages = extract_content(pdf_file)
    return {"pages": all_pages}
