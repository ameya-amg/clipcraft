"""
Advanced SubStation Alpha (.ass) subtitle generator with word-level highlight animation.
Produces high-impact vertical video captions (TikTok / Reels / Shorts style).
"""

import re
from typing import List, Dict, Any


def hex_to_ass_color(hex_str: str, alpha: str = "00") -> str:
    """
    Converts #RRGGBB hex color to ASS format &HAABBGGRR&
    """
    hex_clean = hex_str.strip().lstrip("#")
    if len(hex_clean) == 3:
        hex_clean = "".join(c * 2 for c in hex_clean)
    if len(hex_clean) != 6:
        return f"&H{alpha}FFFFFF&"
    r = hex_clean[0:2]
    g = hex_clean[2:4]
    b = hex_clean[4:6]
    return f"&H{alpha}{b.upper()}{g.upper()}{r.upper()}&"


def format_ass_timestamp(seconds: float) -> str:
    """
    Converts seconds float to ASS timestamp format: H:MM:SS.cc
    """
    if seconds < 0:
        seconds = 0
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    centis = int(round((seconds - int(seconds)) * 100))
    if centis >= 100:
        centis = 99
    return f"{hrs}:{mins:02d}:{secs:02d}.{centis:02d}"


def group_words_into_chunks(words: List[Dict[str, Any]], max_words: int = 3, max_duration: float = 2.5) -> List[List[Dict[str, Any]]]:
    """
    Groups individual timestamped words into punchy 2-4 word visual chunks
    ideal for vertical 9:16 mobile viewing.
    """
    if not words:
        return []

    chunks = []
    current_chunk = []
    chunk_start = None

    for w in words:
        word_text = w.get("word", "").strip()
        if not word_text:
            continue

        w_start = w.get("start", 0.0)
        w_end = w.get("end", w_start + 0.3)

        if not current_chunk:
            chunk_start = w_start
            current_chunk.append({**w, "word": word_text, "start": w_start, "end": w_end})
            continue

        time_gap = w_start - current_chunk[-1]["end"]
        chunk_duration = w_end - chunk_start

        # Break chunk if:
        # 1. Punctuation ending (. ? !)
        # 2. Too many words
        # 3. Time gap between words is significant (>0.5s pause)
        # 4. Total chunk duration exceeds max_duration
        has_period = re.search(r"[.?!]$", current_chunk[-1]["word"])

        if len(current_chunk) >= max_words or has_period or time_gap > 0.45 or chunk_duration > max_duration:
            chunks.append(current_chunk)
            current_chunk = [{**w, "word": word_text, "start": w_start, "end": w_end}]
            chunk_start = w_start
        else:
            current_chunk.append({**w, "word": word_text, "start": w_start, "end": w_end})

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def generate_ass_subtitles(
    words: List[Dict[str, Any]],
    output_path: str,
    font_family: str = "Montserrat-Black",
    font_size: int = 40,
    primary_color: str = "#FFFFFF",
    highlight_color: str = "#FFEA00",
    outline_color: str = "#000000",
    outline_width: int = 5,
    all_caps: bool = True,
    max_words_per_segment: int = 3,
    position_y: int = 72,
    video_width: int = 1080,
    video_height: int = 1920
) -> str:
    """
    Generates a high-quality ASS subtitle file with animated word-level highlighting.
    """
    # Font normalization for libass compatibility
    if font_family in ("Montserrat", "Montserrat Black", "Montserrat-Black"):
        font_name = "Montserrat-Black"
    elif font_family in ("Arial Black", "Arial-Black"):
        font_name = "Arial Black"
    else:
        font_name = font_family

    ass_primary = hex_to_ass_color(primary_color)
    ass_highlight = hex_to_ass_color(highlight_color)
    ass_outline = hex_to_ass_color(outline_color)
    ass_shadow = hex_to_ass_color("#000000", alpha="60")

    # Calculate vertical margin (Alignment 2 = bottom centered)
    # position_y is percentage from top (e.g. 62% means bottom margin is ~38%)
    margin_v = int(video_height * (1.0 - (position_y / 100.0)))
    if margin_v < 60:
        margin_v = 60

    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {video_width}
PlayResY: {video_height}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font_name},{font_size},{ass_primary},&H000000FF,{ass_outline},{ass_shadow},-1,0,0,0,100,100,0,0,1,{outline_width},3,2,60,60,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    chunks = group_words_into_chunks(words, max_words=max_words_per_segment)
    dialogues = []

    for c_idx, chunk in enumerate(chunks):
        chunk_word_count = len(chunk)
        if chunk_word_count == 0:
            continue

        next_chunk_start = None
        if c_idx + 1 < len(chunks) and len(chunks[c_idx + 1]) > 0:
            next_chunk_start = chunks[c_idx + 1][0]["start"]

        for i, current_w in enumerate(chunk):
            w_start = current_w["start"]
            w_end = current_w["end"]

            # If there's a subsequent word in this chunk, stretch this word's end to next word's start
            # so there's no visual flicker between words
            if i + 1 < chunk_word_count:
                display_end = chunk[i + 1]["start"]
            else:
                display_end = w_end + 0.12
                if next_chunk_start is not None and display_end > next_chunk_start:
                    display_end = next_chunk_start

            if display_end <= w_start:
                display_end = w_start + 0.15

            start_str = format_ass_timestamp(w_start)
            end_str = format_ass_timestamp(display_end)

            # Build line text where current word is highlighted with pop effect
            formatted_words = []
            for j, w in enumerate(chunk):
                raw_text = w["word"].strip()
                if all_caps:
                    raw_text = raw_text.upper()

                if j == i:
                    # Active word: Highlight color + 108% scale punch
                    formatted_words.append(f"{{\\c{ass_highlight}\\fscx108\\fscy108}}{raw_text}{{\\r}}")
                else:
                    # Inactive word: Primary base color
                    formatted_words.append(f"{{\\c{ass_primary}}}{raw_text}{{\\r}}")

            line_text = " ".join(formatted_words)
            dialogues.append(f"Dialogue: 0,{start_str},{end_str},Default,,0,0,0,,{line_text}")

    content = header + "\n".join(dialogues) + "\n"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return output_path
