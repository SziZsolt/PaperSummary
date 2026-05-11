import tempfile
import sys
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import Union
from pypdf import PdfReader

ROOT_DIR = Path(__file__).resolve().parents[1]
AI_APP_DIR = ROOT_DIR / "AI" / "app"
sys.path.append(str(AI_APP_DIR))

from ai_engine import PDFSummarizerAI

app = FastAPI(title="PaperSummary Backend")
ai_engine = PDFSummarizerAI()

domains = [
        {"id": "nlp", "label": "Natural Language Processing"},
        {"id": "robotics", "label": "Robotics"},
    ]

def process_pdf(path: Union[str, Path]) -> str:
    """Extract text from a PDF file at `path` and return it as a string.

    Uses pypdf (if available). Falls back to returning the raw bytes decoded
    with replacement characters if extraction fails.
    """
    print("Starting PDF extraction", flush=True)
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
            print("PDF extraction finished", flush=True)
            return joined
    except Exception as e:
        return f"[unextractable PDF: {e}]"


async def save_upload_to_temp(upload_file: UploadFile, suffix: str) -> str:
    """Save an UploadFile to a temporary file and return the path.

    The function reads the upload asynchronously and writes to a NamedTemporaryFile
    (delete=False so the caller can control when it's removed).
    """
    print("Saving the uploaded PDF", flush=True)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    try:
        contents = await upload_file.read()
        tmp.write(contents)
        tmp.flush()
        return tmp.name
    finally:
        print("PDF Saving finished", flush=True)
        tmp.close()


@app.on_event("startup")
def load_ai_model():
    print("Loading AI engine", flush=True)
    ai_engine.load_models()

@app.get("/")
def root():
    return {"status": "ok", "message": "PaperSummary backend is running"}


@app.get("/domains")
def list_domains():
    """Return available domains (id + human label)."""
    return domains


@app.post("/summarize")
async def summarize(file: UploadFile = File(...), domain_id: str = Form(...)):
    """Accept a domain string and a PDF file (both required). Returns a dummy summary.

    Form data (multipart/form-data):
    - domain_id: str (required, must be one of the IDs from /domains)
    - file: UploadFile (required) - expected to be a PDF
    """
    print("REQUEST RECEIVED", flush=True)
    if domain_id not in {d["id"] for d in domains}:
        return JSONResponse(
            {"error": f"Invalid domain_id '{domain_id}'. Must be one of {[d['id'] for d in domains]}"},
            status_code=400,
        )
    original_filename: str = file.filename
    suffix = Path(file.filename).suffix or ".pdf"
    tmp_path = await save_upload_to_temp(file, suffix)
    print("Filename created", flush=True)
    text = process_pdf(tmp_path)
    print("TEXT EXTRACTED:", len(text), flush=True)
    summary = ai_engine.generate_summary(text=text, domain=domain_id)
    print("SUMMARY GENERATED", flush=True)
    try:
        os.unlink(tmp_path)
    except Exception:
        pass

    return JSONResponse(
        {
            "domain": domain_id,
            "filename": original_filename,
            "summary": summary,
        }
    )
