import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# Load hidden variables from .env
load_dotenv()

# Handle /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "👋 **Welcome to the Smart Converter!**\n\n"
        "I am ready when you are. To get started, **simply upload a file** (PDF, HEIC, WEBP, CSV, etc.) into this chat.\n\n"
        "I will detect the format automatically and show you your options."
    )
    
    keyboard = [[InlineKeyboardButton("📋 View All Conversions", callback_data="show_all")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

# Handle inline menu button clicks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer() 
    
    if query.data == "show_all":
        help_text = (
            "🎯 **Here is everything I can do:**\n\n"
            "📄 **Documents:** PDF to Word, Images to PDF\n"
            "🖼️ **Images:** HEIC/WEBP to JPG/PNG\n"
            "📊 **Data:** CSV to Excel\n\n"
            "👇 *Ready? Just upload your file directly into this chat!*"
        )
        await query.edit_message_text(help_text, parse_mode="Markdown")

# Main startup loop
if __name__ == '__main__':
    print("Bot is booting up...")
    
    token = os.getenv("BOT_TOKEN")
    
    if not token:
        print("❌ ERROR: No BOT_TOKEN found. Check your .env file!")
        exit()
        
    app = ApplicationBuilder().token(token).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("✅ Bot is now live and listening!")
    app.run_polling()