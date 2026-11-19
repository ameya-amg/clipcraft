"""
Devanagari to natural Hinglish transliteration engine for Hindi/Hinglish creators.
Maps Hindi spoken content into clean, readable Latin alphabet (Roman script).
"""

import re
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

# Frequent Hindi & Indian Gaming Vocabulary mappings
COMMON_HINDI_SLANG = {
    # Gaming & Tech
    "जीटीए": "GTA",
    "जीटीएक्स": "GTX",
    "गेम": "game",
    "गेमिंग": "gaming",
    "गेमप्ले": "gameplay",
    "वीडियो": "video",
    "ट्रेलर": "trailer",
    "ग्राफिक्स": "graphics",
    "चैनल": "channel",
    "सब्सक्राइब": "subscribe",
    "लाइक": "like",
    "कमेंट": "comment",
    "शेयर": "share",
    "कंप्यूटर": "computer",
    "पीसी": "PC",
    "मिशन": "mission",
    "कैरेक्टर": "character",

    # Pronouns & People
    "भाई": "bhai",
    "यार": "yaar",
    "दोस्त": "dost",
    "लोग": "log",
    "लोगों": "logon",
    "अरे": "arey",
    "मैं": "main",
    "मुझे": "mujhe",
    "मेरा": "mera",
    "मेरी": "meri",
    "मेरे": "mere",
    "हम": "hum",
    "हमें": "humein",
    "हमारा": "hamara",
    "तू": "tu",
    "तुझे": "tujhe",
    "तेरा": "tera",
    "तेरी": "teri",
    "तेरे": "tere",
    "तुम": "tum",
    "तुम्हें": "tumhein",
    "तुम्हारी": "tumhari",
    "तुम्हारा": "tumhara",
    "आप": "aap",
    "आपको": "aapko",
    "आपका": "aapka",
    "यह": "yeh",
    "ये": "yeh",
    "वह": "woh",
    "वो": "woh",
    "इस": "is",
    "इसको": "isko",
    "इससे": "isse",
    "उस": "us",
    "उसको": "usko",
    "उससे": "usse",

    # Common Verbs & Auxiliaries
    "है": "hai",
    "हैं": "hain",
    "हो": "ho",
    "हूँ": "hoon",
    "था": "tha",
    "थी": "thi",
    "थे": "the",
    "नहीं": "nahi",
    "हाँ": "haan",
    "ना": "na",
    "कर": "kar",
    "करना": "karna",
    "करते": "karte",
    "करती": "karti",
    "करता": "karta",
    "किया": "kiya",
    "किये": "kiye",
    "रहा": "raha",
    "रही": "rahi",
    "रहे": "rahe",
    "गया": "gaya",
    "गई": "gayi",
    "गए": "gaye",
    "आया": "aaya",
    "आई": "aayi",
    "आए": "aaye",
    "होगा": "hoga",
    "होगी": "hogi",
    "होंगे": "honge",
    "सकता": "sakta",
    "सकती": "sakti",
    "सकते": "sakte",
    "देखा": "dekha",
    "देखो": "dekho",
    "देख": "dekh",
    "देखते": "dekhte",
    "सुना": "suna",
    "सुनो": "suno",
    "सुन": "sun",
    "बोला": "bola",
    "बोलो": "bolo",
    "बोल": "bol",
    "चल": "chal",
    "चलो": "chalo",
    "बताओ": "batao",
    "बता": "bata",
    "समझ": "samajh",
    "समझे": "samjhe",

    # Adjectives, Conjunctions & Modifiers
    "क्या": "kya",
    "क्यों": "kyun",
    "कैसे": "kaise",
    "कब": "kab",
    "कहाँ": "kahan",
    "कहा": "kahan",
    "कौन": "kaun",
    "और": "aur",
    "लेकिन": "lekin",
    "मगर": "magar",
    "क्योंकि": "kyunki",
    "अगर": "agar",
    "तो": "toh",
    "भी": "bhi",
    "ही": "hi",
    "में": "mein",
    "पर": "par",
    "से": "se",
    "को": "ko",
    "का": "ka",
    "की": "ki",
    "के": "ke",
    "बहुत": "bahut",
    "ज्यादा": "zyada",
    "कम": "kam",
    "अच्छा": "achha",
    "अच्छी": "achhi",
    "अच्छे": "achhe",
    "बुरा": "bura",
    "मस्त": "mast",
    "शानदार": "shandaar",
    "पागल": "pagal",
    "सच": "sach",
    "झूठ": "jhooth",
    "आज": "aaj",
    "कल": "kal",
    "अब": "ab",
    "तब": "tab",
    "सब": "sab",
    "कुछ": "kuch",
    "कोई": "koi",
    "बस": "bas",
    "सिर्फ": "sirf",
    "एक": "ek",
    "दो": "do",
    "तीन": "teen",
    "चार": "chaar",
    "पाँच": "paanch",
    "छह": "che",
    "६": "6",
}


def to_hinglish_word(word: str) -> str:
    """
    Converts a single word from Devanagari to natural Hinglish.
    Preserves English words and numbers unchanged.
    """
    raw = word.strip()
    if not raw:
        return ""

    # Split punctuation boundaries
    match = re.match(r"^([^\w\u0900-\u097F]*)([\w\u0900-\u097F]+)([^\w\u0900-\u097F]*)$", raw)
    if not match:
        return raw

    prefix, core, suffix = match.groups()

    # If no Devanagari characters, return as is
    if not re.search(r"[\u0900-\u097F]", core):
        return raw

    # Check common slang dictionary
    if core in COMMON_HINDI_SLANG:
        return prefix + COMMON_HINDI_SLANG[core] + suffix

    # Fallback to ITRANS transliteration
    try:
        roman = transliterate(core, sanscript.DEVANAGARI, sanscript.ITRANS)
    except Exception:
        roman = core

    # Natural phonetic cleanup
    phonetic_fixes = [
        (r'([a-zA-Z])AI', r'\1ai'),
        (r'Akhir', 'aakhir'),
        (r'yaha\b', 'yeh'),
        (r'vaha\b', 'woh'),
        (r'aura\b', 'aur'),
        (r'kareM\b', 'karein'),
        (r'haiM\b', 'hain'),
        (r'meM\b', 'mein'),
        (r'kA\b', 'ka'),
        (r'kI\b', 'ki'),
        (r'ke\b', 'ke'),
        (r'gayA\b', 'gaya'),
        (r'gayI\b', 'gayi'),
        (r'gaye\b', 'gaye'),
        (r'rahA\b', 'raha'),
        (r'rahI\b', 'rahi'),
        (r'rahe\b', 'rahe'),
        (r'ThIka\b', 'theek'),
        (r'bhAI\b', 'bhai'),
        (r'bahuta\b', 'bahut'),
        (r'shAnadAra', 'shandaar'),
        (r'jITIe', 'GTA'),
        (r'jITI', 'GTA'),
    ]
    for pat, rep in phonetic_fixes:
        roman = re.sub(pat, rep, roman, flags=re.IGNORECASE)

    return prefix + roman.lower() + suffix


def convert_words_to_hinglish(words_list):
    """
    Takes a list of word dicts [{"word": "भाई", "start": 0.1, "end": 0.4}, ...]
    and converts the "word" fields to natural Hinglish.
    """
    converted = []
    for w in words_list:
        orig = w.get("word", "")
        hinglish = to_hinglish_word(orig)
        converted.append({
            **w,
            "word": hinglish
        })
    return converted
