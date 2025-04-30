from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool
from .utils.process_pdf import process_pdf
import base64
import os


API_KEY = os.getenv("API_KEY", "default-secret-key")


async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key


class PdfRequest(BaseModel):
    pdf_base64: str
    page_from: Optional[int] = None
    page_to: Optional[int] = None


app = FastAPI()


@app.get("/health")
async def health_check():
    return {"status": "OK"}


@app.post("/convert")
async def convert(request: PdfRequest, api_key: str = Depends(verify_api_key)):
    pdf_bytes = base64.b64decode(request.pdf_base64)
    pages = await run_in_threadpool(
        process_pdf, pdf_bytes, request.page_from, request.page_to
    )
    return {"pages": pages}
