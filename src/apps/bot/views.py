import json
import logging

from django.http import JsonResponse
from django.views import View
from telegram import Update

from .bot import bot_app

logger = logging.getLogger(__name__)


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
