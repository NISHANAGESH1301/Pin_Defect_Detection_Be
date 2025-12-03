from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from anomaly_graph import router as anomaly_router
from yolo_image import router as yolo_image
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200","http://localhost:4204"],  # Angular URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(anomaly_router)
app.include_router(yolo_image)