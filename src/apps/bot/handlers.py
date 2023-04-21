import json
import logging

from django.conf import settings
from django.urls import reverse
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from apps.core.services.spreadsheets import AsyncGoogleFormSubmitter
from apps.core.services.spreadsheets.runner import send_to_google_sheets
from apps.registration.utils import webapp

from .models import CoverageArea, Fund

AGE = "age"
LOCATION = "location"
COUNTRY = "country"
REGION = "region"
CITY = "city"
FUND = "fund"
NEW_FUND = "new_fund"
NAME = "name"
URL = "URL"
MAIN_DISPLAY_REGIONS = ("Москва", "Московская область", "Санкт-Петербург")

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Start steps")
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
        async for region in CoverageArea.objects.filter(name__in=MAIN_DISPLAY_REGIONS).all()
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
    if update.callback_query.data in MAIN_DISPLAY_REGIONS:
        return await fund(update, context)
    return await region(update, context)


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
    webapp_url_new_fund = f"{settings.WEBHOOK_URL}" f"{reverse('new_fund', args=[context.user_data.get(AGE)])}"
    await webapp(update, context, webapp_url_new_fund)
    return NEW_FUND


async def read_new_fund_form(update: Update, context: ContextTypes.DEFAULT_TYPE):
    json.loads(update.effective_message.web_app_data.data)
    # TODO: передать данные из формы в google таблицу
    data = json.loads(update.effective_message.web_app_data.data)
    table_row = list(data.values())
    values = [table_row]
    await send_to_google_sheets(values, spreadsheetid=settings.SPREADSHEET_ID)
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
    regions_buttons = [
        [InlineKeyboardButton(region.name, callback_data=region.name)]
        async for region in CoverageArea.objects.filter(level=1).exclude(name__in=MAIN_DISPLAY_REGIONS)
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
    if await Fund.objects.filter(
        coverage_area__name=update.callback_query.data,
        age_limit__from_age__lte=context.user_data[AGE],
        age_limit__to_age__gte=context.user_data[AGE],
    ).aexists():
        return await fund(update, context)
    elif await CoverageArea.objects.filter(parent__name=update.callback_query.data).aexists():
        return await city(update, context)
    return await no_fund(update, context)


async def city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button_list = [
        [InlineKeyboardButton(city.name, callback_data=city.name)]
        async for city in CoverageArea.objects.filter(parent__name=context.user_data[REGION])
    ]
    button_list.append([InlineKeyboardButton("Нет моего города", callback_data="no_fund")])
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("Выбери город", reply_markup=InlineKeyboardMarkup(button_list))
    return CITY


async def check_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[CITY] = update.callback_query.data
    region_from_mtpp = await CoverageArea.objects.aget(name=context.user_data[REGION])
    city_from_mtpp = await CoverageArea.objects.aget(name=context.user_data[CITY])
    if (
        region_from_mtpp.id == city_from_mtpp.parent_id
        and await Fund.objects.filter(
            coverage_area__name=context.user_data[CITY],
            age_limit__from_age__lte=context.user_data[AGE],
            age_limit__to_age__gte=context.user_data[AGE],
        ).aexists()
    ):
        return await fund(update, context)
    return await no_fund(update, context)


async def fund(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if CITY not in context.user_data:
        context.user_data[CITY] = update.callback_query.data
    if FUND in context.user_data:
        del context.user_data[FUND]
    fund_list = [
        [InlineKeyboardButton("Почитать про фонды", callback_data="info")],
    ]
    fund_list.extend(
        [
            [InlineKeyboardButton(fund.name, callback_data=fund.name)]
            async for fund in Fund.objects.filter(
                coverage_area__name=context.user_data[CITY],
                age_limit__from_age__lte=context.user_data[AGE],
                age_limit__to_age__gte=context.user_data[AGE],
            )
        ]
    )
    fund_list.append(
        [InlineKeyboardButton("Изменить город?", callback_data="change_city")],
    )
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Фонды, доступные в твоем городе",
        reply_markup=InlineKeyboardMarkup(fund_list),
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
    age = context.user_data.get(AGE)
    region = context.user_data.get(REGION, " ")
    city = context.user_data.get(CITY, " ")
    fund = context.user_data.get(FUND).get("name")
    webapp_url_user = f"{settings.WEBHOOK_URL}" f"{reverse('new_user', args=[age, region, city, fund])}"
    await webapp(update, context, webapp_url_user)
    return FUND


async def read_fund_form(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = json.loads(update.effective_message.web_app_data.data)
    back = data.get("back")
    if back is not None:
        return await location(update, context)  # must be a method fund, but it doesn't work - filtration problem
    google_form = AsyncGoogleFormSubmitter()
    form_data = {
        "surname": data.get("surname", ""),
        "first_name": data.get("name", ""),
        "patronymic": data.get("patronimic", ""),
        "age": context.user_data.get("age", ""),
        "country": context.user_data.get("country", ""),
        "region": context.user_data.get("region", ""),
        "city": context.user_data.get("city", ""),
        "job": data.get("occupation", ""),
        "email": data.get("email", ""),
        "phone": data.get("phone_number", ""),
        "fund_name": context.user_data.get("fund", {}).get("name", ""),
    }
    await google_form.submit_form(form_data)
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
