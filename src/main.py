from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool
from .utils.process_pdf import process_pdf
import base64


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
    pages = await run_in_threadpool(
        process_pdf, pdf_bytes, request.page_from, request.page_to
    )
    return {"pages": pages}
