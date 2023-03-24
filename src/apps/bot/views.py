import json

from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views import View
from django.shortcuts import render
from telegram import Update

from .bot import bot_app
from .logger import logger
from config import settings as s


class BotWebhookView(View):
    try:

        async def post(self, request, *args, **kwargs):
            await bot_app.update_queue.put(
                Update.de_json(
                    data=json.loads(request.body),
                    bot=bot_app.bot,
                )
            )
            return JsonResponse({})

    except Exception as error:
        logger.error(error, exc_info=True)


def rendering(
    request: HttpRequest,
    template_name: str,
    user_data_keys: tuple[str],
) -> HttpResponse:
    ERROR = "Такого поля нет в Контексте"
    context = {}
    for key in user_data_keys:
        context[key] = s.USER_DATA.get(key, ERROR)
    return render(request, template_name, context)


def registration_new_fund(request: HttpRequest) -> HttpResponse:
    template_name = 'registration_new_fund.html'
    user_data_keys = ("age",)
    return rendering(request, template_name, user_data_keys)


def registration_new_user(request: HttpRequest) -> HttpResponse:
    template_name = 'registration_new_user.html'
    user_data_keys = ("age", "region", "city", "fund")
    return rendering(request, template_name, user_data_keys)
