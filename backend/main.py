from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
import uvicorn

from core.logging_config import setup_logging
from core.config import setup_cors
from services.video_generator import generate_segments_zip, get_progress

logger = setup_logging()
app = FastAPI()
setup_cors(app)


@app.post("/generate")
async def generate_videos(
    audio: UploadFile = File(...),
    video: UploadFile = File(...),
    parts: int = Form(...),
    language: str = Form("fr"),
):
    logger.info(
        "Received /generate request: parts=%s, language=%s, audio=%s, video=%s",
        parts,
        language,
        audio.filename,
        video.filename,
    )

    if parts < 1 or parts > 30:
        logger.error("Invalid parts value: %s", parts)
        raise HTTPException(status_code=400, detail="parts must be between 1 and 30")

    zip_buffer = await generate_segments_zip(
        audio=audio,
        video=video,
        parts=parts,
        language=language,
    )

    headers = {"Content-Disposition": 'attachment; filename="videos.zip"'}
    logger.info("Sending zip response")
    return StreamingResponse(zip_buffer, media_type="application/zip", headers=headers)


@app.get("/progress")
def progress():
    data = get_progress()
    return JSONResponse(data)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
