import logging
import io
from telegram import Update, constants
from telegram.ext import ContextTypes
from services.ai_service import AIService
from utils.decorators import anti_spam_cooldown

logger = logging.getLogger(__name__)
ai_service = AIService()

async def process_image_request(update: Update, context: ContextTypes.DEFAULT_TYPE, prompt: str, style_prefix: str = "") -> None:
    """Core function to safely route generation requests, handle state UI, and handle errors."""
    user = update.effective_user
    logger.info(f"User ID: {user.id} (@{user.username}) requested: '{prompt}' with style prefix '{style_prefix}'")

    if not prompt.strip():
        await update.message.reply_text("❌ Your prompt cannot be empty!")
        return

    # User Status Feedback: Notify typing/upload status
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.UPLOAD_PHOTO)
    status_message = await update.message.reply_text("🎨 *Generating image...* Please wait.", parse_mode=constants.ParseMode.MARKDOWN)

    try:
        # Call AI Core
        image_bytes = await ai_service.generate_image(prompt, style_prefix)
        
        # Stream image to memory buffer
        image_file = io.BytesIO(image_bytes)
        image_file.name = "generated_image.png"

        # Send photo back
        await update.message.reply_photo(
            photo=image_file,
            caption=f"✨ \"{prompt}\" Generated successfully!"
        )
    except Exception as e:
        logger.error(f"Error handling generation request: {str(e)}")
        await update.message.reply_text(f"❌ Sorry, generation failed.\nReason: {str(e)}")
    finally:
        # Clean up processing status text
        try:
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=status_message.message_id)
        except Exception:
            pass

@anti_spam_cooldown
async def handle_text_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processes plain-text incoming messages."""
    prompt = update.message.text
    await process_image_request(update, context, prompt)

@anti_spam_cooldown
async def handle_style_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processes direct /anime, /realistic, and /cinematic style commands."""
    command = update.message.text.split()[0].lower()
    prompt = update.message.text.replace(command, "", 1).strip()
    
    style_map = {
        "/anime": "In high-quality clean anime style, illustration, vibrant masterpiece art,",
        "/realistic": "Hyper-realistic ultra-detailed 8k photograph, lifelike, highly detailed texture,",
        "/cinematic": "Cinematic composition, dramatic lighting, movie scene snapshot, epic scope, 35mm lens effect,"
    }
    
    prefix = style_map.get(command, "")
    await process_image_request(update, context, prompt, style_prefix=prefix)
