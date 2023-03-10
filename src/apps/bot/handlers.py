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
    text = "В каком ты городе?"
    regions_buttons = [
        [InlineKeyboardButton(region.name, callback_data=region.name)]
        async for region in CoverageArea.objects.filter(level=1)
    ]
    regions_buttons.extend(
        (
            [InlineKeyboardButton("Другой город", callback_data="other_city")],
            [InlineKeyboardButton("Я не в России", callback_data="other_country")],
        )
    )
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
    else:
        context.user_data[REGION] = update.callback_query.data
        return await city(update, context)


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
    json.loads(update.effective_message.web_app_data.data)
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
    from .models import CoverageArea

    regions_buttons = [
        [InlineKeyboardButton(region.name, callback_data=region.name)]
        async for region in CoverageArea.objects.filter(level=1)
    ]
    regions_buttons.extend(
        [
            [
                InlineKeyboardButton("Далее", callback_data="next"),
                InlineKeyboardButton("Назад", callback_data="prev"),
            ],
            [InlineKeyboardButton("Нет моего региона", callback_data="no_fund")],
        ]
    )
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Выбери регион",
        reply_markup=InlineKeyboardMarkup(regions_buttons),
    )
    return REGION


async def check_region(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[REGION] = update.callback_query.data
    if update.callback_query.data not in ("Москва", "Санкт-Петербург"):
        return await city(update, context)
    return await fund(update, context)


async def city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from .models import CoverageArea

    city = await CoverageArea.objects.aget(parent__name=context.user_data[REGION])
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Выбери город",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(city.name, callback_data=city.name)],
                [InlineKeyboardButton("Нет моего города", callback_data="no_fund")],
            ]
        ),
    )
    return CITY


async def check_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from .models import CoverageArea

    context.user_data[CITY] = update.callback_query.data
    region_from_mtpp = await CoverageArea.objects.aget(name=context.user_data[REGION])
    city_from_mtpp = await CoverageArea.objects.aget(name=context.user_data[CITY])
    if region_from_mtpp.id == city_from_mtpp.parent_id:
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
