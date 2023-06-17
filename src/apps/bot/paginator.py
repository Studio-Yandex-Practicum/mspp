from django.conf import settings
from telegram import InlineKeyboardButton

page = 0


async def paginate(quary, callback_query_data: str, exit_message: str, exit_callback_data: str):
    global page
    if callback_query_data == "next":
        page += 1
    elif callback_query_data == "prev":
        page -= 1
    else:
        page = 0
    if len(quary) < settings.PAGINATION_LIMIT:
        item_buttons = [[InlineKeyboardButton(item.name, callback_data=item.name)] for item in quary]
        item_buttons.extend([[InlineKeyboardButton(exit_message, callback_data=exit_callback_data)]])
        return item_buttons
    item_buttons = [
        [InlineKeyboardButton(item.name, callback_data=item.name)]
        for item in quary[
            page * settings.PAGINATION_LIMIT : page * settings.PAGINATION_LIMIT + settings.PAGINATION_LIMIT
        ]
    ]
    items_count = len(item_buttons)
    item_buttons.extend(
        [
            [
                InlineKeyboardButton("Далее", callback_data="next"),
                InlineKeyboardButton("Назад", callback_data="prev"),
            ],
            [InlineKeyboardButton(exit_message, callback_data=exit_callback_data)],
        ]
    )
    if items_count < settings.PAGINATION_LIMIT and page == 0:
        del item_buttons[-2]
    elif items_count < settings.PAGINATION_LIMIT and page > 0:
        del item_buttons[-2][0]
    elif page == 0:
        del item_buttons[-2][1]
    return item_buttons
