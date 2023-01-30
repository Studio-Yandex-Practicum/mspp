from telegram.ext import Application

from .handlers import HANDLERS
from .settings import TELEGRAM_TOKEN, WEBHOOK_MODE, WEBHOOK_URL

bot_app = Application.builder().token(TELEGRAM_TOKEN).build()
bot_app.add_handlers(HANDLERS)


async def start_bot():
    await bot_app.initialize()
    if WEBHOOK_MODE:
        await bot_app.bot.set_webhook(WEBHOOK_URL)
    else:
        await bot_app.updater.start_polling()
    await bot_app.start()
