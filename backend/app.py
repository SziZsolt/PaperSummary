import tempfile
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import os
from typing import Union
from pypdf import PdfReader

app = FastAPI(title="PaperSummary Backend")

def generate_summary(content: str, domain: str) -> str:
    """Simple dummy summarizer for the MVP.

    Replace this with real model inference later.
    """
    return f"Dummy summary for domain '{domain}'. Received content length: {len(content)}"

def process_pdf(path: Union[str, Path]) -> str:
    """Extract text from a PDF file at `path` and return it as a string.

    Uses pypdf (if available). Falls back to returning the raw bytes decoded
    with replacement characters if extraction fails.
    """
    try:
        reader = PdfReader(str(path))
        texts = []
        for page in reader.pages:
            try:
                txt = page.extract_text() or ""
            except Exception:
                txt = ""
            texts.append(txt)
        joined = "\n".join(texts).strip()
        if joined:
            return joined
    except Exception as e:
        return f"[unextractable PDF: {e}]"

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

    text = process_pdf(tmp.name)
    dummy_summary = generate_summary(content=text, domain=domain)
    try:
        os.unlink(tmp.name)
    except Exception:
        pass

    return JSONResponse(
        {
            "domain": domain,
            "filename": original_filename,
            "summary": dummy_summary,
        }
    )
