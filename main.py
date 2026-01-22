from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from yolo_image import router as yolo_image
#from camera import router as camera_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200","http://localhost:4204"],  # Angular URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(yolo_image)
#app.include_router(camera_router)
