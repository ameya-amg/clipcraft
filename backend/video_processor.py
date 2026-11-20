"""
FFmpeg video processing engine:
1. Re-formats landscape video to 9:16 (1080x1920) using:
   - Blurred Background (best for gaming clips / GTA VI)
   - Center Crop (zoomed in portrait)
   - Black Bars / Fit
2. Dynamic Punch Zooms (Pan / Zoom-in cuts on punchlines / motion)
3. Sound Effects (SFX) mix on transition punchlines (whoosh, pop, ding)
4. Burns in ASS animated subtitles with custom fonts and colors.
"""

import os
import shutil
import subprocess
from typing import Optional, List


def get_ffmpeg_path() -> str:
    # Priority: shutil.which, ffmpeg-full (macOS), then standard Linux/brew paths
    which_ffmpeg = shutil.which("ffmpeg")
    if which_ffmpeg and os.path.exists(which_ffmpeg):
        return which_ffmpeg

    for path in [
        "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg",
        "/usr/bin/ffmpeg",
        "/usr/local/bin/ffmpeg",
        "/opt/homebrew/bin/ffmpeg",
        "ffmpeg"
    ]:
        if os.path.exists(path):
            return path
    return "ffmpeg"


def build_9_16_filter(layout_mode: str = "blurred_bg", punch_zoom: bool = True) -> str:
    """
    Returns the FFmpeg video filter for 9:16 (1080x1920) transformation
    with dynamic punch zoom motion.
    """
    # Zoom expression: cycles every 5.5s, punching in by 1.2x between 2.2s and 4.4s
    zoom_crop_fg = "crop='w=iw/if(between(mod(t,5.5),2.2,4.4),1.2,1.0):h=ih/if(between(mod(t,5.5),2.2,4.4),1.2,1.0):x=(iw-ow)/2:y=(ih-oh)/2',scale=1080:-2"

    if layout_mode == "blurred_bg":
        fg_filter = zoom_crop_fg if punch_zoom else "scale=1080:-2"
        return (
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            "boxblur=25:5[bg];"
            f"[0:v]{fg_filter}[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1[basev]"
        )
    elif layout_mode == "center_crop":
        if punch_zoom:
            return (
                "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
                "crop='w=1080/if(between(mod(t,5.5),2.2,4.4),1.2,1.0):h=1920/if(between(mod(t,5.5),2.2,4.4),1.2,1.0):x=(iw-ow)/2:y=(ih-oh)/2',"
                "scale=1080:1920,setsar=1[basev]"
            )
        else:
            return "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1[basev]"
    else:  # "fit_bars"
        return (
            "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,"
            "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,setsar=1[basev]"
        )


def process_video_to_short(
    input_video_path: str,
    output_video_path: str,
    subtitle_ass_path: Optional[str] = None,
    layout_mode: str = "blurred_bg",
    punch_zoom: bool = True,
    enable_sfx: bool = True,
    sfx_timestamps: Optional[List[float]] = None,
    start_time: Optional[float] = None,
    duration: Optional[float] = None,
    fonts_dir: Optional[str] = None,
    sfx_dir: Optional[str] = None
) -> str:
    """
    Converts input video into 9:16 vertical format with punch zooms,
    burns in animated subtitles, and mixes in punchline sound effects.
    """
    if not os.path.exists(input_video_path):
        raise FileNotFoundError(f"Input video not found: {input_video_path}")

    ffmpeg = get_ffmpeg_path()
    os.makedirs(os.path.dirname(output_video_path), exist_ok=True)

    base_filter = build_9_16_filter(layout_mode=layout_mode, punch_zoom=punch_zoom)

    # Subtitles filter escaping for FFmpeg (escape : and \)
    if subtitle_ass_path and os.path.exists(subtitle_ass_path):
        escaped_ass = subtitle_ass_path.replace("\\", "/").replace(":", "\\:")
        sub_opts = f"subtitles='{escaped_ass}'"
        if fonts_dir and os.path.exists(fonts_dir):
            escaped_fonts = fonts_dir.replace("\\", "/").replace(":", "\\:")
            sub_opts += f":fontsdir='{escaped_fonts}'"
        v_filter_graph = f"{base_filter};[basev]{sub_opts}[v]"
    else:
        v_filter_graph = f"{base_filter};[basev]copy[v]"

    # Prepare SFX mixing
    extra_inputs = []
    audio_filter_graph = None

    if enable_sfx and sfx_timestamps and sfx_dir and os.path.exists(sfx_dir):
        valid_events = []
        last_t = -10.0

        for item in sfx_timestamps:
            if isinstance(item, (list, tuple)) and len(item) == 2:
                ts, sfx_name = float(item[0]), str(item[1])
            else:
                ts, sfx_name = float(item), "pop"

            if ts >= 0.3 and (ts - last_t) >= 1.8:
                if duration is None or ts < (duration - 0.3):
                    valid_events.append((ts, sfx_name))
                    last_t = ts
            if len(valid_events) >= 12:
                break

        if valid_events:
            sfx_filter_chains = []
            input_labels = ["[0:a]"]
            for i, (ts, sfx_name) in enumerate(valid_events):
                sound_path = os.path.join(sfx_dir, f"{sfx_name}.wav")
                if not os.path.exists(sound_path):
                    sound_path = os.path.join(sfx_dir, "pop.wav")

                extra_inputs.extend(["-i", sound_path])
                sfx_idx = 1 + i
                ms = int(round(ts * 1000))
                vol = 0.65 if sfx_name in ("impact", "whoosh") else 0.50
                sfx_filter_chains.append(f"[{sfx_idx}:a]adelay={ms}|{ms},volume={vol}[sfx{i}]")
                input_labels.append(f"[sfx{i}]")

            total_inputs = len(input_labels)
            amix_expr = "".join(input_labels) + f"amix=inputs={total_inputs}:dropout_transition=0:normalize=0[aout]"
            audio_filter_graph = ";".join(sfx_filter_chains) + (";" if sfx_filter_chains else "") + amix_expr

    cmd = [ffmpeg, "-y"]

    if start_time is not None and start_time > 0:
        cmd.extend(["-ss", str(start_time)])

    cmd.extend(["-i", input_video_path])

    if extra_inputs:
        cmd.extend(extra_inputs)

    if duration is not None and duration > 0:
        cmd.extend(["-t", str(duration)])

    if audio_filter_graph:
        full_filter_complex = f"{v_filter_graph};{audio_filter_graph}"
        cmd.extend([
            "-filter_complex", full_filter_complex,
            "-map", "[v]",
            "-map", "[aout]"
        ])
    else:
        cmd.extend([
            "-filter_complex", v_filter_graph,
            "-map", "[v]",
            "-map", "0:a?"
        ])

    cmd.extend([
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "22",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        output_video_path
    ])

    print(f"Running FFmpeg command:\n{' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"FFmpeg stderr:\n{result.stderr}")
        raise RuntimeError(f"FFmpeg failed with exit code {result.returncode}: {result.stderr[-500:]}")

    if not os.path.exists(output_video_path):
        raise RuntimeError("FFmpeg completed but output file was not created.")

    return output_video_path
