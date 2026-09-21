import os
import asyncio
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
from datetime import datetime

load_dotenv()

# Import your newly created business logic module
import converters

load_dotenv()

# --- HANDLER 1: /start Command ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "👋 **Welcome to the Universal File Converter!**\n\n"
        "Send your file or photo directly to this chat:\n"
        "• **Documents:** PDF, Word (`.docx`)\n"
        "• **Images:** JPG, PNG, WEBP, HEIC, or Mobile Photos\n"
        "• **Data:** CSV, Excel (`.xlsx`, `.xls`)\n\n"
        "I will detect the format and show available conversion options."
    )
    keyboard = [[InlineKeyboardButton("📋 View All Conversions", callback_data="show_all")]]
    await update.message.reply_text(
        welcome_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# --- HANDLER 2: File Uploads ---
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    document = update.message.document

    MAX_FILE_SIZE = 20 * 1024 * 1024
    if document.file_size and document.file_size > MAX_FILE_SIZE:
        size_mb = round(document.file_size / (1024 * 1024), 2)
        await update.message.reply_text(
            f"⚠️ **File too large ({size_mb} MB)!**\n\n"
            "Due to Telegram Bot API constraints, files must be under **20 MB** to convert.",
            parse_mode="Markdown"
        )
        return
    
    file_name = document.file_name
    _, extension = os.path.splitext(file_name)
    extension = extension.lower()

    # Store file metadata in temporary memory for the button handler
    context.user_data["file_id"] = document.file_id
    context.user_data["file_name"] = file_name
    context.user_data["extension"] = extension

    buttons = []

    # Dynamic Menu Routing
    if extension == ".pdf":
        buttons.append([InlineKeyboardButton("📄 Convert to Word (.docx)", callback_data="convert_pdf_to_docx")])
        buttons.append([InlineKeyboardButton("🖼️ Convert to Images (.zip)", callback_data="convert_pdf_to_zip")])
        text = f"📎 Received: `{file_name}`\nFormat: **PDF**"

    elif extension in [".png", ".jpg", ".jpeg", ".webp", ".heic"]:
        buttons.append([InlineKeyboardButton("📑 Convert to PDF", callback_data="convert_img_to_pdf")])
        if extension != ".png":
            buttons.append([InlineKeyboardButton("🖼️ Convert to PNG", callback_data="convert_img_to_png")])
        if extension not in [".jpg", ".jpeg"]:
            buttons.append([InlineKeyboardButton("🖼️ Convert to JPG", callback_data="convert_img_to_jpg")])
        text = f"📎 Received: `{file_name}`\nFormat: **Image ({extension.upper().replace('.', '')})**"

    elif extension == ".csv":
        buttons.append([InlineKeyboardButton("📊 Convert to Excel (.xlsx)", callback_data="convert_csv_to_xlsx")])
        text = f"📎 Received: `{file_name}`\nFormat: **CSV Spreadsheet**"

    elif extension in [".xlsx", ".xls"]:
        buttons.append([InlineKeyboardButton("📄 Convert to CSV (.csv)", callback_data="convert_xlsx_to_csv")])
        text = f"📎 Received: `{file_name}`\nFormat: **Excel Workbook**"

    elif extension == ".docx":
        buttons.append([InlineKeyboardButton("📄 Convert to PDF", callback_data="convert_docx_to_pdf")])
        text = f"📎 Received: `{file_name}`\nFormat: **Word Document**"

   
    else:
        clean_ext = extension if extension else "Unknown"
        await update.message.reply_text(
            f"❌ **Unsupported file format (`{clean_ext}`)**\n\n"
            "Please send a supported document (PDF, DOCX), spreadsheet (CSV, Excel), or image.\n\n"
            "Use /start to view all supported formats.",
            parse_mode="Markdown"
        )
        return

    reply_markup = InlineKeyboardMarkup(buttons) if buttons else None
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")


async def handle_unknown_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Guides users when they send non-command text."""
    await update.message.reply_text(
        "👋 **Universal Converter**\n\n"
        "Send me a file or photo directly, or use /start to see the menu.",
        parse_mode="Markdown"
    )


# --- HANDLER: Mobile / Compressed Photos ---
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Telegram sends multiple sizes; the last item [-1] is the highest resolution
    photo = update.message.photo[-1]
    file_name = f"photo_{photo.file_unique_id[:6]}.jpg"

    # Store photo details in session memory
    context.user_data["file_id"] = photo.file_id
    context.user_data["file_name"] = file_name
    context.user_data["extension"] = ".jpg"

    # Offer relevant conversion options
    buttons = [
        [InlineKeyboardButton("📑 Convert to PDF", callback_data="convert_img_to_pdf")],
        [InlineKeyboardButton("🖼️ Convert to PNG", callback_data="convert_img_to_png")]
    ]

    text = f"📷 Received photo (`{file_name}`).\nChoose an option below:"
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="Markdown")


# --- HANDLER 3: Button Clicks & Conversion ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "show_all":
        roster_text = (
            "🎯 **Supported Conversions:**\n\n"
            "📄 **PDF:**\n"
            "  • Convert to Word (`.docx`)\n"
            "  • Render pages to Images (`.zip`)\n\n"
            "📝 **Word (.docx):**\n"
            "  • Convert to PDF\n\n"
            "🖼️ **Images (JPG, PNG, WEBP, HEIC & Mobile Photos):**\n"
            "  • Convert to PDF\n"
            "  • Convert to PNG\n"
            "  • Convert to JPG\n\n"
            "📊 **Spreadsheets:**\n"
            "  • CSV ➔ Excel (`.xlsx`)\n"
            "  • Excel (`.xlsx`, `.xls`) ➔ CSV\n\n"
            "👉 *Upload any file or photo above to get started!*"
        )
        await query.edit_message_text(roster_text, parse_mode="Markdown")
        return

    file_id = context.user_data.get("file_id")
    file_name = context.user_data.get("file_name")

    if not file_id or not file_name:
        await query.edit_message_text("⚠️ File session expired. Please re-upload your file.")
        return

    base_name, _ = os.path.splitext(file_name)
    input_path = f"temp_{file_name}"
    output_path = None

    await query.edit_message_text("⏳ Processing your conversion...")
    print(f"[{datetime.now()}] Request: {query.data} | File: {file_name} | User: {update.effective_user.id}")

    try:
        # Step 1: Download from Telegram
        telegram_file = await context.bot.get_file(file_id)
        await telegram_file.download_to_drive(input_path)

        # Step 2: Route to the correct function in converters.py
        if query.data == "convert_pdf_to_docx":
            output_path = f"temp_{base_name}.docx"
            await asyncio.to_thread(converters.convert_pdf_to_word, input_path, output_path)

        elif query.data == "convert_img_to_pdf":
            output_path = f"temp_{base_name}.pdf"
            await asyncio.to_thread(converters.convert_image_to_pdf, input_path, output_path)

        elif query.data == "convert_img_to_png":
            output_path = f"temp_{base_name}.png"
            await asyncio.to_thread(converters.convert_image_format, input_path, output_path, "PNG")

        elif query.data == "convert_img_to_jpg":
            output_path = f"temp_{base_name}.jpg"
            await asyncio.to_thread(converters.convert_image_format, input_path, output_path, "JPEG")

        elif query.data == "convert_csv_to_xlsx":
            output_path = f"temp_{base_name}.xlsx"
            await asyncio.to_thread(converters.convert_csv_to_excel, input_path, output_path)

        elif query.data == "convert_xlsx_to_csv":
            output_path = f"temp_{base_name}.csv"
            await asyncio.to_thread(converters.convert_excel_to_csv, input_path, output_path)

        elif query.data == "convert_docx_to_pdf":
            output_path = f"temp_{base_name}.pdf"
            await asyncio.to_thread(converters.convert_word_to_pdf, input_path, output_path)

        elif query.data == "convert_pdf_to_zip":
            output_path = f"temp_{base_name}_images.zip"
            await asyncio.to_thread(converters.convert_pdf_to_zip, input_path, output_path)
        # ==========================================

        # Step 3: Upload the converted file back to the chat
        if output_path and os.path.exists(output_path):
            with open(output_path, "rb") as converted_file:
                await context.bot.send_document(
                    chat_id=query.message.chat_id,
                    document=converted_file,
                    filename=os.path.basename(output_path).replace("temp_", ""),
                    caption="✅ Here is your converted document!"
                )
            await query.delete_message()
            print(f"[{datetime.now()}] Success: {query.data}")
        else:
            raise Exception("Output file was not generated.")

    except Exception as e:
        await query.edit_message_text(f"❌ Conversion failed: {str(e)}")
        print(f"[{datetime.now()}] Failed: {query.data} | Error: {str(e)}")

    finally:
        # Step 4: Cleanup temporary files from your laptop
        for path in [input_path, output_path]:
            if path and os.path.exists(path):
                os.remove(path)


# --- MAIN BOOT LOOP ---
if __name__ == '__main__':
    print("Bot is booting up...")
    token = os.getenv("BOT_TOKEN")
    
    if not token:
        print("❌ ERROR: No BOT_TOKEN found.")
        exit()

    app = ApplicationBuilder().token(token).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_unknown_text))

    print("✅ Universal Converter Bot is live and Modular!")
    app.run_polling()