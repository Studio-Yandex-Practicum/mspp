from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    Update,
    WebAppInfo,
)
from telegram.ext import ContextTypes


class UserData:
    data: dict = {}


async def webapp(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    url: str,
    message_text: str = "Нажмите на кнопку ниже, чтобы заполнить анкету",
    button_text: str = "Заполнить анкету",
) -> None:
    await update.callback_query.answer()
    await update.callback_query.delete_message()
    UserData.data = context.user_data
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message_text,
        reply_markup=ReplyKeyboardMarkup.from_button(
            KeyboardButton(
                button_text,
                web_app=WebAppInfo(url=url),
            )))
