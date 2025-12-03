from fastapi import APIRouter, UploadFile, File
from ultralytics import YOLO
import numpy as np
import cv2

router = APIRouter(prefix="/yolo")

# Load model once
model = YOLO("runs/detect/train/weights/best.pt")

@router.post("/predict_image")     # FIXED — remove duplicate /yolo
async def predict_image(file: UploadFile = File(...)):
    # Read bytes
    data = await file.read()

    # Convert bytes → numpy array
    np_arr = np.frombuffer(data, np.uint8)

    # Decode image
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is None:
        return {"error": "Invalid image or format not supported"}

    # Run YOLO prediction
    results = model.predict(img, conf=0.30, imgsz=640)[0]

    detections = []
    for box in results.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        x1, y1, x2, y2 = map(float, box.xyxy[0].tolist())

        detections.append({
            "class": results.names[cls],
            "confidence": conf,
            "bbox": [x1, y1, x2, y2]
        })

    return {
        "detections": detections,
        "count": len(detections)
    }
