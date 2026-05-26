import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, status
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

# Initialize python-telegram-bot Application instance globally
tg_app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

# Register core system commands
tg_app.add_handler(CommandHandler("start", start_command))
tg_app.add_handler(CommandHandler("help", help_command))

# Register style specific commands
tg_app.add_handler(CommandHandler(["anime", "realistic", "cinematic"], handle_style_command))

# Register standard message catchers
tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_prompt))

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manages FastAPI lifespan hooks - Configures and tears down Webhooks safely."""
    # Build webhook target endpoint URL structure
    webhook_url = f"{settings.WEBHOOK_URL}/webhook"
    logger.info(f"Setting Telegram Webhook URL to: {webhook_url}")
    
    await tg_app.initialize()
    await tg_app.bot.set_webhook(url=webhook_url, drop_pending_updates=True)
    
    yield # API running window frame
    
    logger.info("Tearing down application components...")
    await tg_app.bot.delete_webhook()
    await tg_app.shutdown()

app = FastAPI(lifespan=lifespan)

@app.post("/webhook")
async def telegram_webhook_endpoint(request: Request):
    """Processes incoming data directly dropped off by Telegram servers."""
    try:
        json_data = await request.json()
        update = Update.de_json(data=json_data, bot=tg_app.bot)
        await tg_app.process_update(update)
        return Response(status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error parsing incoming updates through API webhook router: {str(e)}")
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

@app.get("/health")
async def health_check():
    """Simple application up-time health check verification routing."""
    return {"status": "healthy"}
