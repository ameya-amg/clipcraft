"""
YouTube downloader and metadata extractor using yt-dlp.
"""

import os
import uuid
import yt_dlp
from typing import Dict, Any, Optional


import certifi

# Configure SSL certificates for macOS Python environment
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()


def get_video_info(url: str) -> Dict[str, Any]:
    """
    Fetches video metadata (title, duration, thumbnail, author, channel)
    without downloading the media file.
    """
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "nocheckcertificate": True,
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web"]
            }
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title", "YouTube Video"),
            "duration": info.get("duration", 0),
            "thumbnail": info.get("thumbnail", ""),
            "channel": info.get("uploader", "Unknown Creator"),
            "id": info.get("id", ""),
            "description": (info.get("description", "") or "")[:200]
        }


def download_youtube_video(
    url: str,
    output_dir: str,
    start_time: Optional[float] = None,
    end_time: Optional[float] = None,
    ffmpeg_location: str = "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"
) -> str:
    """
    Downloads YouTube video (and optionally trims segment).
    Returns path to downloaded MP4 file.
    """
    os.makedirs(output_dir, exist_ok=True)
    video_id = str(uuid.uuid4())[:8]
    output_template = os.path.join(output_dir, f"{video_id}.%(ext)s")

    ydl_opts: Dict[str, Any] = {
        "format": "bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "outtmpl": output_template,
        "quiet": False,
        "no_warnings": True,
        "merge_output_format": "mp4",
        "nocheckcertificate": True,
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web"]
            }
        }
    }

    if os.path.exists(ffmpeg_location):
        ydl_opts["ffmpeg_location"] = os.path.dirname(ffmpeg_location)

    # If partial download requested (yt-dlp download_ranges)
    if start_time is not None and end_time is not None and end_time > start_time:
        def range_callback(info_dict, ydl_instance):
            return [{"start_time": start_time, "end_time": end_time}]
        ydl_opts["download_ranges"] = range_callback
        ydl_opts["force_keyframes_at_cuts"] = True

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        # Find the actual written filename
        filename = ydl.prepare_filename(info)
        base, _ = os.path.splitext(filename)
        mp4_path = f"{base}.mp4"
        if os.path.exists(mp4_path):
            return mp4_path
        elif os.path.exists(filename):
            return filename
        else:
            # Fallback search in directory
            for f in os.listdir(output_dir):
                if f.startswith(video_id):
                    return os.path.join(output_dir, f)
            raise RuntimeError(f"Downloaded file not found for template {output_template}")
