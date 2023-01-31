import json

from django.http import JsonResponse
from django.views import View
from telegram import Update

from .bot import bot_app


class BotWebhookView(View):
    async def post(self, request, *args, **kwargs):
        await bot_app.update_queue.put(
            Update.de_json(
                data=json.loads(request.body),
                bot=bot_app.bot,
            )
        )
        return JsonResponse({})
