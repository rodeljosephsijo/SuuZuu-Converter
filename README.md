# SuuZuu - Telegram Converter Bot 🤖

SuuZuu is a robust Python-based Telegram bot that handles fast, seamless file conversions directly within your chat — deployed and live, not just local code.

🔗 **Try it now:** [t.me/Suu_Zuu_Bot](https://t.me/Suu_Zuu_Bot)

## 🚀 Features

- **Document Conversion:** PDF ↔ Word (`.docx`), PDF → images (`.zip`)
- **Spreadsheet Conversion:** CSV ↔ Excel (`.xlsx`)
- **Image Processing:** HEIC/PNG/JPG/WEBP format handling, mobile photo support
- **Smart Guards:** Built-in 20MB file size limit and unsupported format detection
- **Request Logging:** Every conversion is logged server-side for monitoring and usage visibility

## 🛠️ Tech Stack

- Python 3.11
- `python-telegram-bot` (v20+)
- `PyMuPDF`, `pdf2docx`, `pandas`, `openpyxl`, `Pillow`, `pillow-heif`
- **LibreOffice** (headless) for DOCX → PDF conversion
- Docker for containerized, cross-platform deployment

## ☁️ Deployment

Deployed on [Railway](https://railway.app) using a Docker container that installs LibreOffice for reliable, Linux-compatible document conversion, running as a background worker (not a web service).

## ⚙️ Local Setup

1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file and add your Telegram bot token: `BOT_TOKEN=your_token_here`
4. Run the bot: `python bot.py`

## 🚢 Deploy Your Own

1. Fork/clone this repo
2. Push to your own GitHub
3. Connect the repo to Railway (or Render) as a **worker service**, not a web service
4. Set the `BOT_TOKEN` environment variable in your host's dashboard
5. Deploy — the platform auto-detects the Dockerfile and builds it

## 📦 Project Status

Actively deployed and tested end-to-end. Built as part of an ongoing effort to ship real, usable tools rather than isolated scripts.