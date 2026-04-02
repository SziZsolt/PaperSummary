# AI Service

## Build the Docker image

From the project root:

```bash
docker build -t ai-service ./ai
```

## Run the container

Make sure your Hugging Face token is set in `ai/.env`.

Example `.env`:

```env
HUGGINGFACE_HUB_TOKEN=hf_your_token_here
HF_TOKEN=hf_your_token_here
```

Run with GPU access:

```bash
docker run --rm --gpus all --env-file ai/.env ai-service
```

## What the container does

The image starts `app/smoke_test.py`, which:

1. loads the base model
2. loads the adapters
3. runs a small inference test
4. prints the generated summary

If the run succeeds and prints a summary, the image is working