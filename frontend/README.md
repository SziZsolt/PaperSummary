# PaperSummary — Frontend (Vue + Vite)

Minimal frontend to upload a PDF and a domain string, then display the summary returned by the backend.

Quick start

1) From the `frontend/` folder install dependencies:

```bash
cd frontend
npm install
```

2) Run the dev server:

```bash
npm run dev
```

Open http://localhost:5173 in your browser.

Notes
- The frontend posts to `http://127.0.0.1:8000/summarize`. Make sure the backend is running there or update the URL in `PdfUploader.vue`.
- If you hit CORS errors, enable CORS on the backend (FastAPI's `CORSMiddleware`) while developing.
