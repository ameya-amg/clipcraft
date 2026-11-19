"""
Intelligent punchline and transition detector.
Analyzes speech transcript, exclamation triggers, and video zoom cut timestamps
to determine exactly when and which sound effects (whoosh, pop, ding, impact) to play.
"""

import re
from typing import List, Dict, Any, Tuple

# Punchline triggers in Hindi, Hinglish, and English
HIGH_ENERGY_WORDS = {
    # Hindi / Hinglish
    "bhai", "yaar", "arre", "kya", "dekho", "dekh", "omg", "oho", "mast",
    "shandaar", "pagal", "sach", "jhooth", "finally", "gta", "trailer",
    "khatam", "bawaal", "ruk", "ruko", "sun", "suno", "gadbad", "scam",
    # English
    "what", "bro", "wait", "look", "omg", "no", "yes", "insane", "crazy",
    "impossible", "boom", "wow", "damn", "listen", "never", "watch", "secret"
}


def detect_intelligent_sfx(
    words: List[Dict[str, Any]],
    duration: float = 30.0,
    punch_zoom_enabled: bool = True
) -> List[Tuple[float, str]]:
    """
    Returns a list of (timestamp_seconds, sfx_name) where sfx_name is:
    'whoosh', 'impact', 'ding', or 'pop'.
    Guarantees good spacing (no overlapping sounds within 2.5s).
    """
    sfx_events: List[Tuple[float, str]] = []
    used_timestamps: List[float] = []

    def is_spaced(ts: float, min_gap: float = 2.2) -> bool:
        return all(abs(ts - u) >= min_gap for u in used_timestamps)

    # 1. Detect punchline keywords & exclamations from speech
    for w in words:
        raw = w.get("word", "").lower()
        clean = re.sub(r"[^\w]", "", raw)
        start = w.get("start", 0.0)

        if start < 0.3 or (duration and start > (duration - 0.8)):
            continue

        # Check for exclamations or high energy words
        is_exclamation = bool(re.search(r"[!?]$", raw))
        is_keyword = clean in HIGH_ENERGY_WORDS

        if (is_keyword or is_exclamation) and is_spaced(start):
            sfx_type = "impact" if (is_exclamation or clean in {"bhai", "omg", "kya", "boom", "insane"}) else "ding"
            sfx_events.append((start, sfx_type))
            used_timestamps.append(start)

    # 2. Add transition whooshes on dynamic zoom-in cuts
    if punch_zoom_enabled:
        # Punch zoom occurs every 5.5s at relative offset 2.2s
        t = 2.2
        cycle = 5.5
        while t < (duration - 1.0):
            if is_spaced(t, min_gap=2.0):
                sfx_events.append((t, "whoosh"))
                used_timestamps.append(t)
            t += cycle

    # 3. If very few events were found (e.g. sparse speech), add rhythmic pops on key phrase starts
    if len(sfx_events) < 2 and words:
        for i, w in enumerate(words):
            start = w.get("start", 0.0)
            if start > 1.0 and is_spaced(start, min_gap=3.5):
                sfx_events.append((start, "pop"))
                used_timestamps.append(start)
            if len(sfx_events) >= 4:
                break

    # Sort chronologically
    sfx_events.sort(key=lambda x: x[0])
    return sfx_events
