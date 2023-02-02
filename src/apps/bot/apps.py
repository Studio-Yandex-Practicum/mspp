import asyncio
import logging

from django.apps import AppConfig

from .bot import start_bot


class BotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bot"

    def ready(self) -> None:
        try:
            asyncio.ensure_future(start_bot(), loop=asyncio.get_running_loop())
        except RuntimeError:
            logging.warning("Telegram бот не запущен. Для запуска используйте uvicorn.")
