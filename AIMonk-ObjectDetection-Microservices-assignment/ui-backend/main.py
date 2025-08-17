from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os, uuid, io, json, requests
from PIL import Image, ImageDraw

AI_URL = os.getenv("AI_URL", "http://localhost:8000/detect")

app = FastAPI(title="UI Backend")
templates = Jinja2Templates(directory="templates")

# Serve saved outputs (images + json files)
os.makedirs("outputs", exist_ok=True)
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload(request: Request, file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload an image file.")
    raw = await file.read()

    # Send to AI backend
    try:
        resp = requests.post(AI_URL, files={"file": (file.filename, raw, file.content_type)}, timeout=60)
        resp.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to reach AI backend: {e}")

    data = resp.json()

    # Draw boxes
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    draw = ImageDraw.Draw(img)

    for det in data.get("detections", []):
        box = det["box"]
        x1, y1, x2, y2 = box["x1"], box["y1"], box["x2"], box["y2"]
        # outline and a tiny label background
        draw.rectangle([(x1, y1), (x2, y2)], outline=1, width=3)
        label = f"{det['class_name']} {det['confidence']:.2f}"
        tw, th = draw.textlength(label), 14
        draw.rectangle([(x1, y1 - th - 2), (x1 + tw + 4, y1)], fill=1)
        draw.text((x1 + 2, y1 - th - 2), label)

    # Save outputs
    uid = uuid.uuid4().hex[:8]
    img_name = f"{uid}_{file.filename or 'image.jpg'}"
    img_path = os.path.join("outputs", img_name)
    json_path = os.path.join("outputs", f"{uid}.json")

    img.save(img_path)
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "img_url": f"/outputs/{os.path.basename(img_path)}",
        "json_url": f"/outputs/{os.path.basename(json_path)}",
        "detections": data.get("detections", []),
        "img_w": data.get("image_width"),
        "img_h": data.get("image_height"),
    })
