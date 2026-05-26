import time
from functools import wraps
from collections import defaultdict
from telegram import Update
from telegram.ext import ContextTypes

# Simple in-memory anti-spam cooldown cache: {user_id: last_request_timestamp}
COOLDOWN_TIME = 10  # seconds
user_cooldowns = defaultdict(float)

def anti_spam_cooldown(func):
    """Prevents users from spamming image generation requests."""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if not update.effective_user:
            return
        
        user_id = update.effective_user.id
        current_time = time.time()
        time_passed = current_time - user_cooldowns[user_id]
        
        if time_passed < COOLDOWN_TIME:
            remaining = int(COOLDOWN_TIME - time_passed)
            await update.message.reply_text(
                f"⚠️ Please wait {remaining} seconds before generating another image."
            )
            return
        
        # Update timestamp and execute function
        user_cooldowns[user_id] = current_time
        return await func(update, context, *args, **kwargs)
    return wrapper
