# AIMonk Object Detection Microservices assignment

This repo contains a minimal two-service setup to satisfy the assignment:
- **AI Backend**: FastAPI service exposing `/detect` for object detection using a lightweight YOLO model (Ultralytics). CPU-only by default.
- **UI Backend**: FastAPI service with a simple upload UI. It sends the image to the AI service, draws bounding boxes, saves outputs (image + JSON), and shows results.

## Run locally (Docker recommended)

```bash
# 1) Build and run the stack
docker compose up --build

# 2) Open the UI in your browser
#    http://localhost:8080

# 3) Upload an image and view results
```

Outputs (annotated images + JSON) will appear under `ui-backend/outputs/`.

## Run locally without Docker (for development)

```bash
# In one terminal (AI backend)
cd ai-backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000

# In another terminal (UI backend)
cd ui-backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8080
```

## Deliverables checklist

- [x] Project folder, dockerized for easy replication
- [x] Documentation (this README + per-service READMEs)
- [x] Output images with bounding boxes and corresponding JSON files are generated after each upload (see `ui-backend/outputs/`).
