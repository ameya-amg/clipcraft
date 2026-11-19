# ⚡ ClipCraft AI - GTA VI & Viral Shorts Generator

ClipCraft AI is a 100% free, local-first web application that converts long YouTube videos (such as GTA VI trailers, gameplay, or podcasts) into viral **9:16 vertical Shorts, Reels, and TikToks** with word-by-word animated captions, intelligent punch zooms, and transition sound effects.

---

## ✨ Features

- **YouTube Downloader**: Paste any YouTube video link with automatic range clipping.
- **Word-Level AI Captions**: Powered by `faster-whisper` with real-time active word pop/highlighting (Hormozi / MrBeast style).
- **Hindi & Hinglish Support**: Automatically transcribes spoken Hindi commentary into clean, viral Roman script (Hinglish).
- **Dynamic Punch Zooms**: Automatic camera punch-in/zoom cuts every ~4s for high-retention pacing.
- **Intelligent Sound Effects (SFX)**: Automatic whooshes, impacts, pops, and dings timed to punchlines and camera cuts.
- **Trending Caption Presets**:
  - **Hormozi Viral**: High-contrast white text with neon yellow active-word highlight & thick black outline.
  - **MrBeast Punch**: High-energy comic style with neon lime green highlight.
  - **GTA Vice Neon**: Cyberpunk Miami Vice aesthetic with electric cyan base and hot pink highlight.
  - **Gold & Fire**: Clean base with fiery orange/gold keyword pops.
  - **Clean Minimalist**: Subtle modern sans-serif.
- **Complete Font Size & Style Control**:
  - Direct slider & number input from 36px to 140px.
  - Instant quick-size chips (Small 48px, Medium 65px, Large 85px, Giant/Viral 110px).
  - Works seamlessly across all framing modes including full-screen **Center Crop**.
- **Smart 9:16 Layouts**:
  - **Blurred Background** (Recommended for GTA & gaming gameplay).
  - **Center Crop** (Full-screen portrait).
  - **Fit (Letterbox)**.
- **Live Mobile Mockup**: Interactive phone preview simulating mobile Shorts layout in real-time.

---

## 🚀 Local Quick Start

```bash
cd /Users/ameyagade/.gemini/antigravity/scratch/clipcraft
./run.sh
```

Then open your browser at **`http://localhost:8000`**.

---

## 🌐 Deployment

### 1. Vercel (Frontend & Serverless Edge)
The frontend and presets endpoint are configured for Vercel deployment via `vercel.json`:
```bash
npx vercel --prod
```
When running on Vercel, the web app includes a built-in **AI Engine Connection** dialog to connect to your local machine or cloud container backend.

### 2. Docker / Cloud Backend (Render, Railway, Fly.io)
A production-ready `Dockerfile` is included:
```bash
docker build -t clipcraft .
docker run -p 8000:8000 clipcraft
```

---

## 🛠️ Tech Stack

- **Backend**: Python 3.12, FastAPI, Uvicorn
- **AI Speech-to-Text**: `faster-whisper` (CTranslate2 int8)
- **Transliteration**: `indic-transliteration`
- **Video & Audio Processing**: `yt-dlp`, `ffmpeg` (with `libass` subtitle burn-in, `amix`, `adelay`)
- **Frontend**: Responsive Dark UI, CSS3 live mobile preview, interactive HTML5 video player
