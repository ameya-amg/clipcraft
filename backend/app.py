"""
ClipCraft - FastAPI Application
Converts YouTube videos to 9:16 Shorts with trending auto-captions and customizable styles.
"""

import os
import uuid
import asyncio
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from .presets import PRESETS
from .downloader import get_video_info, download_youtube_video
from .transcriber import transcribe_video_with_words
from .subtitle_generator import generate_ass_subtitles
from .video_processor import process_video_to_short
from .punchline_detector import detect_intelligent_sfx

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORAGE_DIR = os.path.join(BASE_DIR, "storage")
DOWNLOADS_DIR = os.path.join(STORAGE_DIR, "downloads")
OUTPUTS_DIR = os.path.join(STORAGE_DIR, "outputs")
SUBTITLES_DIR = os.path.join(STORAGE_DIR, "subtitles")
STATIC_DIR = os.path.join(BASE_DIR, "static")
FONTS_DIR = os.path.join(STATIC_DIR, "fonts")

SFX_DIR = os.path.join(STATIC_DIR, "sfx")

from fastapi.middleware.cors import CORSMiddleware

for d in [DOWNLOADS_DIR, OUTPUTS_DIR, SUBTITLES_DIR, STATIC_DIR, FONTS_DIR, SFX_DIR]:
    os.makedirs(d, exist_ok=True)

app = FastAPI(title="ClipCraft - GTA VI & Shorts AI Clipper")

# Enable CORS for Vercel and remote frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory job state store
jobs: Dict[str, Dict[str, Any]] = {}


class VideoInfoRequest(BaseModel):
    url: str


class CreateClipRequest(BaseModel):
    url: str
    start_time: Optional[float] = 0.0
    end_time: Optional[float] = 30.0
    preset: Optional[str] = "hormozi"
    font_family: Optional[str] = "Montserrat"
    font_size: Optional[int] = 60
    primary_color: Optional[str] = "#FFFFFF"
    highlight_color: Optional[str] = "#FFEA00"
    outline_color: Optional[str] = "#000000"
    outline_width: Optional[int] = 6
    all_caps: Optional[bool] = True
    max_words_per_segment: Optional[int] = 3
    position_y: Optional[int] = 62
    layout_mode: Optional[str] = "blurred_bg"
    model_size: Optional[str] = "base"
    language: Optional[str] = "hinglish"
    punch_zoom: Optional[bool] = True
    enable_sfx: Optional[bool] = True


@app.get("/api/presets")
def get_presets():
    return JSONResponse(content={"presets": PRESETS})


@app.post("/api/video-info")
def fetch_info(req: VideoInfoRequest):
    try:
        info = get_video_info(req.url)
        return JSONResponse(content={"success": True, "info": info})
    except Exception as e:
        return JSONResponse(status_code=400, content={"success": False, "error": str(e)})


def run_clip_pipeline(job_id: str, req: CreateClipRequest):
    try:
        jobs[job_id]["status"] = "downloading"
        jobs[job_id]["progress"] = 15
        jobs[job_id]["message"] = "Downloading YouTube video stream..."

        # Step 1: Download video (with segment range if specified)
        downloaded_video = download_youtube_video(
            url=req.url,
            output_dir=DOWNLOADS_DIR,
            start_time=req.start_time,
            end_time=req.end_time
        )

        jobs[job_id]["status"] = "transcribing"
        jobs[job_id]["progress"] = 45
        jobs[job_id]["message"] = f"Transcribing speech ({req.language.upper()}) with AI word timestamps..."

        # Step 2: Speech-to-text with word timestamps and Hinglish transliteration
        words = transcribe_video_with_words(
            downloaded_video,
            model_size=req.model_size or "small",
            language=req.language or "hinglish"
        )

        jobs[job_id]["status"] = "generating_subtitles"
        jobs[job_id]["progress"] = 70
        jobs[job_id]["message"] = f"Styling captions ({len(words)} words in Hinglish/English)..."

        # Duration of clip
        duration = None
        if req.end_time and req.start_time is not None:
            duration = max(1.0, req.end_time - req.start_time)

        # Base style from preset, but USER values ALWAYS take priority!
        base_style = PRESETS.get(req.preset, PRESETS["hormozi"]) if (req.preset and req.preset in PRESETS) else {}
        style = {
            "font_family": req.font_family or base_style.get("font_family", "Montserrat"),
            "font_size": req.font_size if req.font_size else base_style.get("font_size", 60),
            "primary_color": req.primary_color or base_style.get("primary_color", "#FFFFFF"),
            "highlight_color": req.highlight_color or base_style.get("highlight_color", "#FFEA00"),
            "outline_color": req.outline_color or base_style.get("outline_color", "#000000"),
            "outline_width": req.outline_width if req.outline_width is not None else base_style.get("outline_width", 6),
            "all_caps": req.all_caps if req.all_caps is not None else base_style.get("all_caps", True),
            "max_words_per_segment": req.max_words_per_segment or base_style.get("max_words_per_segment", 3),
            "position_y": req.position_y if req.position_y is not None else base_style.get("position_y", 62)
        }

        ass_path = os.path.join(SUBTITLES_DIR, f"{job_id}.ass")
        if words:
            generate_ass_subtitles(
                words=words,
                output_path=ass_path,
                font_family=style["font_family"],
                font_size=style["font_size"],
                primary_color=style["primary_color"],
                highlight_color=style["highlight_color"],
                outline_color=style["outline_color"],
                outline_width=style["outline_width"],
                all_caps=style["all_caps"],
                max_words_per_segment=style["max_words_per_segment"],
                position_y=style["position_y"]
            )
        else:
            ass_path = None

        # Intelligent Sound Effects (punchlines, exclamations & zoom cuts)
        sfx_events = []
        if req.enable_sfx:
            sfx_events = detect_intelligent_sfx(
                words=words,
                duration=duration or 30.0,
                punch_zoom_enabled=bool(req.punch_zoom)
            )

        jobs[job_id]["status"] = "rendering"
        jobs[job_id]["progress"] = 85
        jobs[job_id]["message"] = f"Applying punch zooms, {len(sfx_events)} SFX hits & burning captions..."

        output_video_path = os.path.join(OUTPUTS_DIR, f"short_{job_id}.mp4")

        process_video_to_short(
            input_video_path=downloaded_video,
            output_video_path=output_video_path,
            subtitle_ass_path=ass_path,
            layout_mode=req.layout_mode,
            punch_zoom=req.punch_zoom,
            enable_sfx=req.enable_sfx,
            sfx_timestamps=sfx_events,
            duration=duration,
            fonts_dir=FONTS_DIR,
            sfx_dir=SFX_DIR
        )

        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = 100
        jobs[job_id]["message"] = "Ready! Clip generated successfully."
        jobs[job_id]["output_url"] = f"/storage/outputs/short_{job_id}.mp4"
        jobs[job_id]["word_count"] = len(words)

    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["message"] = f"Error: {str(e)}"
        print(f"Job {job_id} failed: {e}")


@app.post("/api/create-clip")
def create_clip(req: CreateClipRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())[:8]
    jobs[job_id] = {
        "id": job_id,
        "status": "queued",
        "progress": 5,
        "message": "Initializing task...",
        "output_url": None
    }
    background_tasks.add_task(run_clip_pipeline, job_id, req)
    return JSONResponse(content={"success": True, "job_id": job_id})


@app.get("/api/job-status/{job_id}")
def get_job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return JSONResponse(content=jobs[job_id])


# Serve generated videos
app.mount("/storage/outputs", StaticFiles(directory=OUTPUTS_DIR), name="outputs")

# Serve frontend static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index():
    root_index = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(root_index):
        return FileResponse(root_index)
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))
