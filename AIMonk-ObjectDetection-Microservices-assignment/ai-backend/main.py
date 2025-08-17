from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List, Dict
from ultralytics import YOLO
import ultralytics
from PIL import Image
import io
import numpy as np
import torch
app = FastAPI(title="AI Backend - Object Detection")

# Load a lightweight model; downloads on first run if not cached.
# Runs on CPU if no GPU is available.
torch.serialization.add_safe_globals([ultralytics.nn.tasks.DetectionModel])

model = YOLO("yolov8n.pt")

class Box(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float

class Detection(BaseModel):
    class_name: str
    confidence: float
    box: Box

class DetectionResponse(BaseModel):
    image_width: int
    image_height: int
    detections: List[Detection]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/detect", response_model=DetectionResponse)
async def detect(file: UploadFile = File(...)):
    # Read image bytes
    img_bytes = await file.read()
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

    # Run inference
    results = model.predict(source=np.array(img), device="cpu", verbose=False)
    result = results[0]

    boxes_xyxy = result.boxes.xyxy.cpu().numpy() if result.boxes is not None else np.empty((0,4))
    clss = result.boxes.cls.cpu().numpy().astype(int).tolist() if result.boxes is not None else []
    confs = result.boxes.conf.cpu().numpy().tolist() if result.boxes is not None else []
    names = result.names

    detections: List[Detection] = []
    for (x1, y1, x2, y2), c, conf in zip(boxes_xyxy, clss, confs):
        detections.append(Detection(
            class_name=names.get(c, str(c)),
            confidence=float(conf),
            box=Box(x1=float(x1), y1=float(y1), x2=float(x2), y2=float(y2))
        ))

    return DetectionResponse(
        image_width=img.width,
        image_height=img.height,
        detections=detections
    )
