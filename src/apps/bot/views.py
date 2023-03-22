import json

from django.http import JsonResponse
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


def registration_form(request):
    ERROR = "Такого поля нет в Контексте"
    template_name = 'registration.html'
    context = {
        "age": s.USER_DATA.get("age", ERROR),
        "region": s.USER_DATA.get("region", ERROR),
        "city": s.USER_DATA.get("city", ERROR),
        "fund": s.USER_DATA.get("fund", {}).get("name", ERROR),
    }
    return render(request, template_name, context)
