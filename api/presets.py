from http.server import BaseHTTPRequestHandler
import json

PRESETS = {
    "hormozi": {
        "name": "Hormozi Viral",
        "font_family": "Montserrat",
        "font_size": 60,
        "primary_color": "#FFFFFF",
        "highlight_color": "#FFEA00",
        "outline_color": "#000000",
        "outline_width": 6,
        "all_caps": True,
        "position_y": 62,
        "max_words_per_segment": 3
    },
    "beast": {
        "name": "MrBeast Punch",
        "font_family": "Anton",
        "font_size": 64,
        "primary_color": "#FFFFFF",
        "highlight_color": "#39FF14",
        "outline_color": "#000000",
        "outline_width": 7,
        "all_caps": True,
        "position_y": 60,
        "max_words_per_segment": 2
    },
    "vice_neon": {
        "name": "GTA Vice Neon",
        "font_family": "Impact",
        "font_size": 62,
        "primary_color": "#00FFFF",
        "highlight_color": "#FF1493",
        "outline_color": "#0D0B18",
        "outline_width": 6,
        "all_caps": True,
        "position_y": 63,
        "max_words_per_segment": 3
    },
    "fire_gold": {
        "name": "Gold & Fire",
        "font_family": "Arial Black",
        "font_size": 58,
        "primary_color": "#FFFFFF",
        "highlight_color": "#FF7700",
        "outline_color": "#000000",
        "outline_width": 6,
        "all_caps": True,
        "position_y": 62,
        "max_words_per_segment": 3
    },
    "minimal_clean": {
        "name": "Clean Minimalist",
        "font_family": "Helvetica",
        "font_size": 50,
        "primary_color": "#F0F0F0",
        "highlight_color": "#FFFFFF",
        "outline_color": "#1A1A1A",
        "outline_width": 4,
        "all_caps": False,
        "position_y": 65,
        "max_words_per_segment": 4
    }
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"presets": PRESETS}).encode('utf-8'))
