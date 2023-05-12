import asyncio
import logging
from http import HTTPStatus
from typing import Any

import aiohttp
from aiogoogle import Aiogoogle, HTTPError
from django.conf import settings

from .auth import creds

logger = logging.getLogger(__name__)


class AsyncGoogleFormSubmitter:
    def __init__(self, form_id: str = settings.GOOGLE_FORM_ID, form_fields: dict = settings.GOOGLE_FORM_FIELDS):
        """Инициализация URL и полей формы."""
        self.form_url = settings.GOOGLE_FORM_URL.format(form_id)
        self.form_fields = form_fields

    async def submit_form(self, data: dict) -> bool:
        """Отправка формы."""
        payload = {f"entry.{self.form_fields[key]}": data[key] for key in self.form_fields.keys() & data.keys()}

        async with aiohttp.ClientSession() as session:
            async with session.post(self.form_url, data=payload) as response:
                logger.info(f"Отправленная форма {self.form_url} со статусом {response.status}.\nС данными {payload}")
                return response.status == HTTPStatus.OK


async def set_user_permissions(
    spreadsheet_id: str,
) -> None:

    permissions_body = {"type": "user", "role": "writer", "emailAddress": settings.EMAIL_USER}
    async with Aiogoogle(service_account_creds=creds) as aiogoogle:
        try:
            service = await aiogoogle.discover("drive", settings.DRIVE_VERS)
            await aiogoogle.as_service_account(
                service.permissions.create(fileId=spreadsheet_id, json=permissions_body, fields="id")
            )
        except HTTPError as e:
            msg = "Не удалось авторизоваться!"
            logger.critical(msg, e)
            raise HTTPError(msg)


async def send(table_values: list[list[Any]], spreadsheet_id: str) -> None:
    """Отправляет переданные данные в Google таблицы.

    Args:
        spreadsheetid (str): ID Google таблицы
        table_values (list[list[Any]]): Значения колонок
    Raises:
        HTTPError: Не удалось отправить сроку в таблицу
    """
    async with Aiogoogle(service_account_creds=creds) as aiogoogle:
        range = f"1:{len(table_values)}"

        update_body = {"majorDimension": "ROWS", "values": table_values}
        try:
            service = await aiogoogle.discover("sheets", settings.SHEETS_VERS)
            await aiogoogle.as_service_account(
                service.spreadsheets.values.append(
                    spreadsheetId=spreadsheet_id, range=range, valueInputOption="USER_ENTERED", json=update_body
                )
            )
        except HTTPError as e:
            msg = "Не удалось отправить сроку в таблицу!"
            logger.critical(msg, e)
            raise HTTPError(msg)
        logger.info(settings.SPREADSHEETS_URL.format(spreadsheet_id))


def sender(
    values: list[list[Any]],
    spreadsheetid: str,
) -> None:
    """Отправляет переданные данные в Google таблицы.

    Args:
        table_values (list[list[Any]]): Значения колонок
        spreadsheetid (str): ID Google таблицы. Defaults to settings.SPREADSHEET_ID.
    Raises:
        HTTPError: Не удалось отправить сроку в таблицу
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.get_event_loop().run_until_complete(send(spreadsheetid, values))
