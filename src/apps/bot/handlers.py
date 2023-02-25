import json

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    WebAppInfo,
)
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

AGE = "age"
LOCATION = "location"
COUNTRY = "country"
REGION = "region"
CITY = "city"
FUND = "fund"
NEW_FUND = "new_fund"
NAME = "name"
URL = "URL"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_html(
        text=(
            "Привет! Я бот проекта ЗНАЧИМ. Я помогу тебе встать на путь "
            "наставничества - стать настоящим другом для подростка, которому "
            "нужна помощь.\n\n"
            "Сначала я помогу тебе выбрать фонд, а затем заполнить небольшую "
            "анкету."
        ),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Понятно", callback_data="age")]]),
    )
    return AGE


async def age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("Сколько тебе лет?")
    return AGE


async def check_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if int(update.message.text) < 18:
        await update.message.reply_html(
            "Извини, но стать наставником ты сможешь только, когда тебе "
            "исполнится 18. А пока, я уверен, ты сможешь найти себя в другом "
            "волонтерском проекте)"
        )
        return ConversationHandler.END
    else:
        context.user_data[AGE] = update.message.text
        return await location(update, context)


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from .models import CoverageArea

    if COUNTRY in context.user_data:
        del context.user_data[COUNTRY]
    if REGION in context.user_data:
        del context.user_data[REGION]
    if CITY in context.user_data:
        del context.user_data[CITY]
    if FUND in context.user_data:
        del context.user_data[FUND]
    print("start user_data:", context.user_data)  # FIXME: удалить
    text = "В каком ты городе?"
    regions_buttons = [
        [InlineKeyboardButton("Другой город", callback_data="other_city")],
        [InlineKeyboardButton("Я не в России", callback_data="other_country")],
    ]
    async for region in CoverageArea.objects._mptt_filter(level=1):
        regions_buttons.insert(0, [InlineKeyboardButton(region.name, callback_data=region.name)])
    keyboard = InlineKeyboardMarkup(regions_buttons)
    if update.message:
        await update.message.reply_html(text=text, reply_markup=keyboard)
    else:
        await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    return LOCATION


async def check_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[COUNTRY] = "Россия"
    if update.callback_query.data == "Москва":
        context.user_data[REGION] = "Московская область"
        context.user_data[CITY] = update.callback_query.data
        return await fund(update, context)
    if update.callback_query.data == "Санкт-Петербург":
        context.user_data[REGION] = update.callback_query.data
        context.user_data[CITY] = update.callback_query.data
        return await fund(update, context)
    if update.callback_query.data == "Московская область":
        context.user_data[REGION] = update.callback_query.data
        return await city(update, context)
    return ConversationHandler.END


async def no_fund(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Извини, на данный момент проект не реализуется в твоем городе, но "
        "мы планируем развиваться! Напиши нам если знаешь благотворительный "
        "фонд, который занимается помощью детям-сиротам и детям, оставшимся "
        "без попечения родителей, чтобы мы запустили проект в твоем городе.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Да, давай", callback_data="new_fund_form")]]),
    )
    return NEW_FUND


async def new_fund_form(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.delete_message()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Нажмите на кнопку ниже, чтобы заполнить анкету",
        reply_markup=ReplyKeyboardMarkup.from_button(
            KeyboardButton(
                "Заполнить анкету",
                # TODO: заменить на веб-приложение с формой
                # Данные для подстановки в форму:
                # context.user_data[AGE] - возраст
                web_app=WebAppInfo(url="https://python-telegram-bot.org/static/webappbot"),
            )
        ),
    )
    return NEW_FUND


async def read_new_fund_form(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("finish user_data:", context.user_data)  # FIXME: удалить
    data = json.loads(update.effective_message.web_app_data.data)
    print("web_app data:", data)  # FIXME: удалить
    # TODO: передать данные из формы в google таблицу
    await update.message.reply_html(
        "Спасибо! Я передал твою заявку. Поcтараемся запустить проект в "
        "твоем городе как можно скорее и обязательно свяжемся с тобой.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


async def country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Выбери страну",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Казахстан", callback_data="Казахстан")],
                # TODO: добавить пагинацию
                [
                    InlineKeyboardButton("Далее", callback_data="next"),
                    InlineKeyboardButton("Назад", callback_data="prev"),
                ],
                [InlineKeyboardButton("Другая страна", callback_data="no_fund")],
            ]
        ),
    )
    return COUNTRY


async def check_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[COUNTRY] = update.callback_query.data
    if update.callback_query.data == "Казахстан":
        return await fund(update, context)
    return ConversationHandler.END


async def region(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Выбери регион",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Регион 1", callback_data="Регион 1")],
                [InlineKeyboardButton("Регион 2", callback_data="Регион 2")],
                [InlineKeyboardButton("Регион 3", callback_data="Регион 3")],
                [InlineKeyboardButton("Регион 4", callback_data="Регион 4")],
                [InlineKeyboardButton("Регион 5", callback_data="Регион 5")],
                [InlineKeyboardButton("Регион 6 (без городов)", callback_data="Регион 6")],
                [InlineKeyboardButton("Регион 7 (без городов)", callback_data="Регион 7")],
                [InlineKeyboardButton("Регион 8 (без городов)", callback_data="Регион 8")],
                [InlineKeyboardButton("Регион 9 (без городов)", callback_data="Регион 9")],
                [InlineKeyboardButton("Регион 10 (без городов)", callback_data="Регион 10")],
                # TODO: добавить пагинацию
                [
                    InlineKeyboardButton("Далее", callback_data="next"),
                    InlineKeyboardButton("Назад", callback_data="prev"),
                ],
                [InlineKeyboardButton("Нет моего региона", callback_data="no_fund")],
            ]
        ),
    )
    return REGION


async def check_region(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[REGION] = update.callback_query.data
    if update.callback_query.data in (
        "Регион 1",
        "Регион 2",
        "Регион 3",
        "Регион 4",
        "Регион 5",
    ):
        return await city(update, context)
    if update.callback_query.data in ("Регион 6", "Регион 7", "Регион 8", "Регион 9", "Регион 10"):
        return await fund(update, context)
    return ConversationHandler.END


async def city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Выбери город",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Город 1", callback_data="Город 1")],
                [InlineKeyboardButton("Город 2", callback_data="Город 2")],
                [InlineKeyboardButton("Город 3", callback_data="Город 3")],
                [InlineKeyboardButton("Город 4", callback_data="Город 4")],
                [InlineKeyboardButton("Город 5", callback_data="Город 5")],
                [InlineKeyboardButton("Город 6", callback_data="Город 6")],
                [InlineKeyboardButton("Город 7", callback_data="Город 7")],
                [InlineKeyboardButton("Город 8", callback_data="Город 8")],
                [InlineKeyboardButton("Город 9", callback_data="Город 9")],
                [InlineKeyboardButton("Город 10", callback_data="Город 10")],
                # TODO: добавить пагинацию
                [
                    InlineKeyboardButton("Далее", callback_data="next"),
                    InlineKeyboardButton("Назад", callback_data="prev"),
                ],
                [InlineKeyboardButton("Нет моего города", callback_data="no_fund")],
            ]
        ),
    )
    return CITY


async def check_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[CITY] = update.callback_query.data
    if update.callback_query.data in (
        "Город 1",
        "Город 2",
        "Город 3",
        "Город 4",
        "Город 5",
        "Город 6",
        "Город 7",
        "Город 8",
        "Город 9",
        "Город 10",
    ):
        return await fund(update, context)
    return ConversationHandler.END


async def fund(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if CITY not in context.user_data:
        context.user_data[CITY] = update.callback_query.data
    if FUND in context.user_data:
        del context.user_data[FUND]
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Фонды, доступные в твоем городе",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Почитать про фонды", callback_data="info")],
                [InlineKeyboardButton("Арифметика добра", callback_data="Арифметика добра")],
                [InlineKeyboardButton("Фонд 2", callback_data="Фонд 2")],
                [InlineKeyboardButton("Фонд 3", callback_data="Фонд 3")],
                [InlineKeyboardButton("Фонд 4", callback_data="Фонд 4")],
                [InlineKeyboardButton("Фонд 5", callback_data="Фонд 5")],
                [InlineKeyboardButton("Фонд 6", callback_data="Фонд 6")],
                [InlineKeyboardButton("Фонд 7", callback_data="Фонд 7")],
                # TODO: пагинация?
                [InlineKeyboardButton("Изменить город?", callback_data="change_city")],
            ]
        ),
    )
    return FUND


async def check_fund(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[FUND] = {NAME: update.callback_query.data}
    if update.callback_query.data == "Арифметика добра":
        context.user_data[FUND][URL] = "https://crm.a-dobra.ru/form/mentor"
    if context.user_data[FUND].get(URL):
        return await fund_has_form(update, context)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Последний шаг - заполним анкету",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Изменить фонд", callback_data="fund")],
                [InlineKeyboardButton("Заполнить анкету", callback_data="fund_form")],
            ]
        ),
    )
    return FUND


async def fund_has_form(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("finish user_data:", context.user_data)  # FIXME: удалить
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "У этого фонда есть своя анкета, заполни ее на сайте фонда по ссылке " f"{context.user_data[FUND][URL]}"
    )
    return ConversationHandler.END


async def fund_form(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.delete_message()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Нажмите на кнопку ниже, чтобы заполнить анкету",
        reply_markup=ReplyKeyboardMarkup.from_button(
            KeyboardButton(
                "Заполнить анкету",
                # TODO: заменить на веб-приложение с формой
                # Данные для подстановки в форму:
                # context.user_data[AGE] - возраст
                # context.user_data[COUNTRY] - страна
                # context.user_data[REGION] - регион, если есть
                # context.user_data[CITY] - город, если есть
                # context.user_data[FUND][NAME] - название фонда
                web_app=WebAppInfo(url="https://python-telegram-bot.org/static/webappbot"),
            )
        ),
    )
    return FUND


async def read_fund_form(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("finish user_data:", context.user_data)  # FIXME: удалить
    data = json.loads(update.effective_message.web_app_data.data)
    print("web_app data:", data)  # FIXME: удалить
    # TODO: передать данные из формы в google таблицу
    await update.message.reply_html(
        "Спасибо! Я передал твою заявку. Фонд свяжется с тобой, чтобы "
        "уточнить детали и пригласить на собеседование.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


async def fund_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "\n\n".join(
            [
                "Арифметка добра - помогает детям-сиротам стать личностью, "
                "поддерживает приемные семьи, содействует семейному устройству.",
                "Старшие братья старшие сестры - подбирает наставников детям и "
                "подросткам, находящихся в трудной жизненной ситуации.",
                "В твоих руках - помогает подросткам, оставшимся без поддержки "
                "родителям, подготовиться к самостоятельной жизни.",
                "Волонтеры в помощь детям-сиротам - помогает детям сиротам в "
                "детских домах и больницах, ищет им приемных родителей и "
                "поддерживает семьи в трудной жизненной ситуации.",
                "Дети+ - оказывает поддержку детям, подросткам и молодым людям с "
                "ВИЧ, семьям, в которых живут дети с ВИЧ.",
                "Дети наши - помогает в социальной адаптации воспитанников "
                "детских домов, поддерживает кризисные семьи.",
                "Солнечный город - помогает детям и семьям, которые оказались в трудной жизненной ситуации.",
            ]
        ),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Понятно", callback_data="fund")]]),
    )
    return FUND


HANDLERS = (
    ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            AGE: [
                CallbackQueryHandler(age, "^age$"),
                MessageHandler(filters.Regex(r"^\d{1,3}$"), check_age),
            ],
            LOCATION: [
                CallbackQueryHandler(region, "^other_city$"),
                CallbackQueryHandler(country, "^other_country$"),
                CallbackQueryHandler(check_location, "^.*$"),
            ],
            COUNTRY: [
                CallbackQueryHandler(no_fund, "^no_fund$"),
                CallbackQueryHandler(country, "^next|prev$"),
                CallbackQueryHandler(check_country, "^.*$"),
            ],
            REGION: [
                CallbackQueryHandler(no_fund, "^no_fund$"),
                CallbackQueryHandler(region, "^next|prev$"),
                CallbackQueryHandler(check_region, "^.*$"),
            ],
            CITY: [
                CallbackQueryHandler(no_fund, "^no_fund$"),
                CallbackQueryHandler(city, "^next|prev$"),
                CallbackQueryHandler(check_city, "^.*$"),
            ],
            FUND: [
                CallbackQueryHandler(location, "^change_city$"),
                CallbackQueryHandler(fund_info, "^info$"),
                CallbackQueryHandler(fund, "^next|prev|fund$"),
                CallbackQueryHandler(fund_form, "^fund_form$"),
                CallbackQueryHandler(check_fund, "^.*$"),
                MessageHandler(filters.StatusUpdate.WEB_APP_DATA, read_fund_form),
            ],
            NEW_FUND: [
                CallbackQueryHandler(new_fund_form, "^new_fund_form$"),
                MessageHandler(
                    filters.StatusUpdate.WEB_APP_DATA,
                    read_new_fund_form,
                ),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    ),
)
