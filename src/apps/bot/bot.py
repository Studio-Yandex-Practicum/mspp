import logging
from urllib.parse import urljoin

from django.conf import settings
from telegram.ext import Application

from .handlers import HANDLERS

logger = logging.getLogger(__name__)

bot_app = Application.builder().token(settings.TELEGRAM_TOKEN).build()
bot_app.add_handlers(HANDLERS)


async def start_bot():
    try:
        await bot_app.initialize()
        if settings.WEBHOOK_MODE:
            await bot_app.bot.set_webhook(urljoin(settings.WEBHOOK_URL, "bot/"))
        else:
            logger.info("Bot started through webhook")
            await bot_app.updater.start_polling()
        logger.info("Bot started through polling")
        await bot_app.start()
    except Exception as error:
        logger.error(error, exc_info=True)
