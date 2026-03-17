"""FastAPI app for PaperSummary (MVP)

This file is a clean runnable FastAPI app. It mirrors the intended behavior of
`backend_main.py` but is created as `backend.app` so we can start the server
without editing the existing malformed file.
"""

import tempfile
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse

app = FastAPI(title="PaperSummary Backend", version="0.1")


def generate_summary(content: str, domain: str) -> str:
    """Simple dummy summarizer for the MVP.

    Replace this with real model inference later.
    """
    return f"Dummy summary for domain '{domain}'. Received content length: {len(content)}"


@app.get("/")
def root():
    return {"status": "ok", "message": "PaperSummary backend is running"}


@app.post("/summarize")
async def summarize(file: UploadFile = File(...), domain: str = Form(...)):
    """Accept a domain string and a PDF file (both required). Returns a dummy summary.

    Form data (multipart/form-data):
    - domain: str (required)
    - file: UploadFile (required) - expected to be a PDF
    """

    original_filename: str = file.filename
    suffix = Path(file.filename).suffix or ".pdf"

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    try:
        contents = await file.read()
        tmp.write(contents)
        tmp.flush()
    finally:
        tmp.close()

    content_str = (
        contents.decode("utf-8", errors="replace")
        if isinstance(contents, (bytes, bytearray))
        else str(contents)
    )

    dummy_summary = generate_summary(content=content_str, domain=domain)

    return JSONResponse(
        {
            "domain": domain,
            "filename": original_filename,
            "summary": dummy_summary,
        }
    )
