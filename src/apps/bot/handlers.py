from telegram import Update
from telegram.ext import CommandHandler, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_html("Test reply message")


HANDLERS = (CommandHandler("start", start),)
