import os
from typing import List, Dict, Any
import av

# PyAV 14+ removed the 'metadata_errors' keyword argument from av.open()
# Monkey-patch av.open to strip metadata_errors cleanly
_orig_av_open = av.open

def _safe_av_open(*args, **kwargs):
    kwargs.pop("metadata_errors", None)
    return _orig_av_open(*args, **kwargs)

av.open = _safe_av_open

from faster_whisper import WhisperModel

from .hinglish import convert_words_to_hinglish

# Cache model instance to avoid re-loading on every clip
_CACHED_MODEL = None
_CURRENT_MODEL_SIZE = None


def get_transcriber_model(model_size: str = "small") -> WhisperModel:
    global _CACHED_MODEL, _CURRENT_MODEL_SIZE
    if _CACHED_MODEL is None or _CURRENT_MODEL_SIZE != model_size:
        try:
            _CACHED_MODEL = WhisperModel(model_size, device="cpu", compute_type="int8")
            _CURRENT_MODEL_SIZE = model_size
        except Exception:
            # Fallback to base model if small is unavailable or still downloading
            _CACHED_MODEL = WhisperModel("base", device="cpu", compute_type="int8")
            _CURRENT_MODEL_SIZE = "base"
    return _CACHED_MODEL


def transcribe_video_with_words(
    video_path: str,
    model_size: str = "small",
    language: str = "auto"
) -> List[Dict[str, Any]]:
    """
    Transcribes audio from a video file and extracts word-level timestamps.
    Automatically supports Hindi -> Hinglish transliteration.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    model = get_transcriber_model(model_size)

    # Prompt conditioning for Hindi/Hinglish speech
    initial_prompt = "Ye video Hindi aur Hinglish me hai. Jo bola gaya hai usko Hinglish Roman script me likho jaise bhai ye kya scene hai, GTA 6 finally aa gaya."

    whisper_lang = None
    if language == "hi" or language == "hinglish":
        whisper_lang = "hi"
    elif language == "en":
        whisper_lang = "en"
        initial_prompt = None

    segments, info = model.transcribe(
        video_path,
        word_timestamps=True,
        language=whisper_lang,
        initial_prompt=initial_prompt,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=300)
    )

    all_words = []
    for segment in segments:
        if segment.words:
            for w in segment.words:
                cleaned_word = w.word.strip()
                if cleaned_word:
                    all_words.append({
                        "word": cleaned_word,
                        "start": round(w.start, 2),
                        "end": round(w.end, 2),
                        "probability": round(w.probability, 2)
                    })
        else:
            words_in_seg = segment.text.strip().split()
            if words_in_seg:
                seg_dur = max(segment.end - segment.start, 0.5)
                dur_per_word = seg_dur / len(words_in_seg)
                for i, w in enumerate(words_in_seg):
                    w_start = segment.start + (i * dur_per_word)
                    w_end = w_start + dur_per_word
                    all_words.append({
                        "word": w,
                        "start": round(w_start, 2),
                        "end": round(w_end, 2),
                        "probability": 1.0
                    })

    # Convert any Devanagari to clean natural Hinglish
    all_words = convert_words_to_hinglish(all_words)

    return all_words
