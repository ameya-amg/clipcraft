"""
Presets for trending subtitle styles (Hormozi, Beast, Vice Neon, Minimal, etc.)
"""

PRESETS = {
    "hormozi": {
        "name": "Hormozi Viral",
        "description": "Thick uppercase text, bright yellow active word highlight, heavy black outline.",
        "font_family": "Montserrat",
        "font_size": 60,
        "primary_color": "#FFFFFF",      # White
        "highlight_color": "#FFEA00",    # Neon Yellow
        "outline_color": "#000000",      # Black
        "outline_width": 6,
        "all_caps": True,
        "max_words_per_segment": 3,
        "position_y": 62,                # % from top (over bottom half of video)
    },
    "beast": {
        "name": "High Energy (MrBeast)",
        "description": "Bold dynamic comic style with punchy lime green active highlight.",
        "font_family": "Anton",
        "font_size": 64,
        "primary_color": "#FFFFFF",
        "highlight_color": "#39FF14",    # Neon Green
        "outline_color": "#000000",
        "outline_width": 7,
        "all_caps": True,
        "max_words_per_segment": 2,
        "position_y": 60,
    },
    "vice_neon": {
        "name": "GTA Vice Neon",
        "description": "Miami / Vice City cyberpunk neon theme with hot pink highlight and cyan base.",
        "font_family": "Impact",
        "font_size": 62,
        "primary_color": "#00FFFF",      # Cyan
        "highlight_color": "#FF1493",    # Hot Pink
        "outline_color": "#0D0B18",      # Deep navy black
        "outline_width": 6,
        "all_caps": True,
        "max_words_per_segment": 3,
        "position_y": 63,
    },
    "fire_gold": {
        "name": "Gold & Fire",
        "description": "Clean white base with blazing orange/gold active keyword highlight.",
        "font_family": "Arial Black",
        "font_size": 58,
        "primary_color": "#FFFFFF",
        "highlight_color": "#FF7700",    # Blazing Orange
        "outline_color": "#000000",
        "outline_width": 6,
        "all_caps": True,
        "max_words_per_segment": 3,
        "position_y": 62,
    },
    "minimal_clean": {
        "name": "Clean Minimalist",
        "description": "Clean modern sans-serif with subtle contrast, perfect for commentary/podcasts.",
        "font_family": "Helvetica",
        "font_size": 50,
        "primary_color": "#F0F0F0",
        "highlight_color": "#FFFFFF",
        "outline_color": "#1A1A1A",
        "outline_width": 4,
        "all_caps": False,
        "max_words_per_segment": 4,
        "position_y": 65,
    }
}
