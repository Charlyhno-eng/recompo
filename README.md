# recompo

Recompo is a small web app that turns one long audio track and one looping visual (GIF or MP4) into multiple short, subtitled clips in English. Each segment gets its own burned‑in subtitles generated with Whisper, making the clips ready for social media.

## Features

- Upload an audio file (MP3) and a visual file (MP4 or GIF).
- Choose how many clips to generate with a slider.
- Automatic segmentation of the audio into equal parts.
- Loop and trim the visual to match each segment duration.
- English subtitles generated with Faster‑Whisper and burned into each clip.
- ZIP download containing all generated videos.

## Requirements

- Python 3.10+
- Node.js and npm (or pnpm / yarn)
- FFmpeg installed and available in your PATH
- Git (optional, for cloning)

## Backend installation

```bash
# 1. Go to backend folder
cd backend

# 2. Create virtual environment
python3 -m venv .venv

# 3. Activate virtual environment
# Linux / macOS:
source .venv/bin/activate
# Windows (PowerShell):
# .venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run backend (FastAPI + Uvicorn)
uvicorn main:app --reload
```

The backend is now available at: http://127.0.0.1:8000.

## Frontend installation

```bash
# 1. Go to frontend folder
cd frontend

# 2. Install dependencies (npm, pnpm or yarn)
npm install

# 3. Run dev server
npm run dev
```

The frontend is now available at: http://localhost:5173.
