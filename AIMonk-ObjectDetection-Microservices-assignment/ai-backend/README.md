# AI Backend

FastAPI service exposing `/detect` that accepts an image and returns detections as JSON.
Uses a lightweight YOLO model (Ultralytics YOLOv8n) and runs on CPU by default.

## API

- `GET /health` → `{"status": "ok"}` for health checks
- `POST /detect` (multipart form):
  - field: `file` → image file
  - response: JSON with `image_width`, `image_height`, and a list of detections:
    ```json
    {
      "image_width": 1280,
      "image_height": 720,
      "detections": [
        {
          "class_name": "person",
          "confidence": 0.90,
          "box": {"x1": 12, "y1": 34, "x2": 100, "y2": 200}
        }
      ]
    }
    ```

## Run

See the top-level README for Docker instructions. To run locally without Docker:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```
