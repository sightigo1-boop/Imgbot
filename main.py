import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config import settings
from handlers.commands import start_command, help_command
from handlers.messages import handle_text_prompt, handle_style_command

# System-wide Logging Configuration
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    """Starts the bot in Long Polling mode (Perfect for Background Workers)."""
    logger.info("Initializing Telegram Bot in Polling Mode...")
    
    # Initialize python-telegram-bot Application instance
    tg_app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

    # Register core system commands
    tg_app.add_handler(CommandHandler("start", start_command))
    tg_app.add_handler(CommandHandler("help", help_command))

    # Register style specific commands
    tg_app.add_handler(CommandHandler(["anime", "realistic", "cinematic"], handle_style_command))

    # Register standard message catchers
    tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_prompt))

    # Clear any old webhooks so polling can take over cleanly
    await tg_app.bot.delete_webhook(drop_pending_updates=True)

    # Start the continuous polling loop
    logger.info("Bot is now live and listening for messages!")
    
    # Run polling loop natively within our async main loop
    async with tg_app:
        await tg_app.start()
        await tg_app.updater.start_polling(drop_pending_updates=True)
        # Keep running until the process is stopped
        while True:
            await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped cleanly.")
