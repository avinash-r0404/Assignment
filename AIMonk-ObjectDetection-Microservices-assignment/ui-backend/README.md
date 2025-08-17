# UI Backend

FastAPI app that renders a simple web form for image upload, calls the AI service, draws bounding boxes, saves outputs, and displays results.

- `GET /` – upload form
- `POST /upload` – handles upload, calls AI service (via `AI_URL` env), draws boxes, saves outputs (image + JSON), and renders `result.html`
- Static outputs are served under `/outputs/*`

To run locally without Docker:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export AI_URL=http://localhost:8000/detect
uvicorn main:app --host 0.0.0.0 --port 8080
```

Then open http://localhost:8080.
