# Running PaperSummary

After cloning the repository, run the following in two separate terminals:

## 1. Backend

Replace `YOUR_HF_TOKEN` with your token. (Ask the team for the access token)

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

Go to `http://localhost:3000`.