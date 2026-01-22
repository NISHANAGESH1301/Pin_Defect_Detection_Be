import subprocess
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(prefix="/camera")

@router.post("/capture")
def capture_image():
    image_path = "/tmp/capture.jpg"

    subprocess.run(
        [
            "fswebcam",
            "--no-banner",
            "-r", "1280x720",
            image_path
        ],
        check=True
    )

    return FileResponse(
        image_path,
        media_type="image/jpeg",
        filename="capture.jpg"
    )
