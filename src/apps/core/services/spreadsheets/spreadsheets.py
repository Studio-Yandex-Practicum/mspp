from http import HTTPStatus

import aiohttp
from django.conf import settings

from .logger import logger


class AsyncGoogleFormSubmitter:
    def __init__(self, form_id: str = settings.GOOGLE_FORM_ID, form_fields: dict = settings.GOOGLE_FORM_FIELDS):
        """Инициализация URL и полей формы."""
        self.form_url = settings.GOOGLE_FORM_URL.format(form_id)
        self.form_fields = form_fields

    async def submit_form(self, data: dict) -> bool:
        """Отправка формы."""
        # Передаются только data ключи совпадающие с ключами в form_fields
        payload = {f"entry.{self.form_fields[key]}": data[key] for key in self.form_fields.keys() & data.keys()}

        # Отправляем POST-запрос на сервер с помощью aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(self.form_url, data=payload) as response:
                logger.info(
                    f"Отправленная форма {self.form_url} со статусом {response.status}/n" f"С данными {payload}"
                )

                return response.status == HTTPStatus.OK
