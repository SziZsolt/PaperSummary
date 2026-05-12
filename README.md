# Team

- **Máté György Gulyás-Szabó** — Integration & Deployment  
- **Zsolt Szigetközi** — Backend  
- **Eltun Salmanli** — Frontend  
- **Martin Mosonyi** — AI  
- **Levente Barta** — AI  

# Prerequisites

Make sure you have Docker installed before building and running the project.

A CUDA-compatible GPU is required to run the backend container, since the AI models are too large to run efficiently on CPU-only systems.

# Building the Docker Images

Run the following commands from the repository root:

```bash
docker build -f frontend_new/Dockerfile -t papersummary-frontend frontend_new

docker build -f backend/Dockerfile -t papersummary-backend .
```

# Running PaperSummary

After building the images, run the following in two separate terminals.

## 1. Backend

Replace `YOUR_HF_TOKEN` with your Hugging Face token.  
(Ask the team for the access token if needed.)

```bash
docker run --rm --gpus all -p 8000:8000 \
  -e HF_TOKEN=YOUR_HF_TOKEN \
  -v hf-cache:/app/.cache/huggingface \
  papersummary-backend
```

## 2. Frontend

```bash
docker run --rm -p 3000:3000 papersummary-frontend
```

## 3. Access

Open:

```text
http://localhost:3000
```