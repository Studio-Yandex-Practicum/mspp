import asyncio

from django.apps import AppConfig


class BotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bot"

    def ready(self) -> None:
        from .bot import start_bot

        asyncio.ensure_future(start_bot(), loop=asyncio.get_event_loop())
