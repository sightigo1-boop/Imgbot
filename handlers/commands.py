from telegram import Update, constants
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /start command."""
    user = update.effective_user.first_name
    welcome_text = (
        f"👋 Hello {user}!\n\n"
        "I am an AI Image Generator Bot. Simply send me a text description, "
        "and I will generate an image for you!\n\n"
        "🎨 **Special Styles Available:**\n"
        "• `/anime [your prompt]`\n"
        "• `/realistic [your prompt]`\n"
        "• `/cinematic [your prompt]`\n\n"
        "Or just send a plain message to generate a standard style image."
    )
    await update.message.reply_text(welcome_text, parse_mode=constants.ParseMode.MARKDOWN)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /help command."""
    help_text = (
        "💡 **How to use me:**\n\n"
        "1. Send a direct text prompt (e.g., `a futuristic city in Mars`)\n"
        "2. Use explicit style modifiers:\n"
        "   • `/anime cyberpunk samurai`\n"
        "   • `/realistic historical library`\n"
        "   • `/cinematic dark knight superhero`\n\n"
        "⚠️ **Rules:**\n"
        "• No empty prompts.\n"
        "• There is a 10-second cooldown protection between generations."
    )
    await update.message.reply_text(help_text, parse_mode=constants.ParseMode.MARKDOWN)
