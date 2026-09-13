import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

# 1. Load the bot token from .env
load_dotenv()

# 2. Command: /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "👋 **Welcome to the Smart Converter!**\n\n"
        "To get started, **upload a file** (PDF, PNG, JPG, or CSV) directly to this chat.\n\n"
        "I will detect the format automatically and show you your conversion options."
    )
    keyboard = [[InlineKeyboardButton("📋 View All Conversions", callback_data="show_all")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

# 3. Button Clicks (Callback Query)
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "show_all":
        help_text = (
            "🎯 **Supported Conversions:**\n\n"
            "📄 **PDF:** Convert to Word (.docx)\n"
            "🖼️ **Images (PNG/JPG):** Convert to PDF\n"
            "📊 **Data (CSV):** Convert to Excel (.xlsx)\n\n"
            "👉 *Send any of these files to try it out!*"
        )
        await query.edit_message_text(help_text, parse_mode="Markdown")

    elif query.data.startswith("convert_"):
        action = query.data.replace("convert_", "")
        await query.edit_message_text(
            f"⚙️ Action selected: **{action.upper()}**\n\n*(Ready to connect conversion engine!)*",
            parse_mode="Markdown"
        )

# 4. File Upload Listener & Extension Router
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    document = update.message.document
    file_name = document.file_name

    # Extract extension safely
    _, extension = os.path.splitext(file_name)
    extension = extension.lower()

    if extension == ".pdf":
        buttons = [
            [InlineKeyboardButton("📄 Convert to Word (.docx)", callback_data="convert_pdf_to_docx")]
        ]
        text = f"📎 Received: `{file_name}`\n\nFormat: **PDF**\nChoose an option below:"

    elif extension in [".png", ".jpg", ".jpeg"]:
        buttons = [
            [InlineKeyboardButton("📑 Convert to PDF", callback_data="convert_img_to_pdf")]
        ]
        text = f"📎 Received: `{file_name}`\n\nFormat: **Image**\nChoose an option below:"

    elif extension == ".csv":
        buttons = [
            [InlineKeyboardButton("📊 Convert to Excel (.xlsx)", callback_data="convert_csv_to_xlsx")]
        ]
        text = f"📎 Received: `{file_name}`\n\nFormat: **CSV Spreadsheet**\nChoose an option below:"

    else:
        buttons = []
        text = f"⚠️ Received: `{file_name}`\n\nSorry, **{extension}** is not supported yet."

    reply_markup = InlineKeyboardMarkup(buttons) if buttons else None
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

# 5. Boot sequence
if __name__ == '__main__':
    print("Bot is booting up...")
    token = os.getenv("BOT_TOKEN")

    if not token:
        print("❌ ERROR: No BOT_TOKEN found. Check your .env file!")
        exit()

    app = ApplicationBuilder().token(token).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    print("✅ Bot is live and listening for files!")
    app.run_polling()