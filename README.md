# SuuZuu - Telegram Converter Bot 🤖

SuuZuu is a robust Python-based Telegram bot designed to handle fast and seamless file conversions directly within your chat. 

## 🚀 Features
* **Document Conversion:** PDF to DOCX, DOCX to PDF.
* **Spreadsheet Conversion:** Excel (.xlsx) to CSV.
* **Image Processing:** HEIC/PNG/JPG format handling.
* **Smart Guards:** Built-in 20MB file size limit and unsupported format detection.

## 🛠️ Tech Stack
* Python 3
* `python-telegram-bot` (v20+)
* `PyMuPDF`, `docx2pdf`, `pandas`, `Pillow`

## ⚙️ Local Setup
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file and add your Telegram bot token: `TELEGRAM_BOT_TOKEN=your_token_here`
4. Run the bot: `python bot.py`