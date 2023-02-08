import asyncio
from typing import Any

from aiogoogle import Aiogoogle, HTTPError
from django.conf import settings

from .auth import creds
from .logger import logger


async def send(
    spreadsheetid: str,
    table_values: list[list[Any]],
) -> None:
    """Отправляет переданные данные в Google таблицы.

    Args:
        spreadsheetid (str): ID Google таблицы
        table_values (list[list[Any]]): Значения колонок

    Raises:
        HTTPError: Не удалось отправить сроку в таблицу
    """
    async with Aiogoogle(service_account_creds=creds) as aiogoogle:
        range = f"1:{len(table_values)}"

        update_body = {"majorDimension": "COLUMNS", "values": table_values}
        try:
            service = await aiogoogle.discover("sheets", "v4")
            await aiogoogle.as_service_account(
                service.spreadsheets.values.append(
                    spreadsheetId=spreadsheetid, range=range, valueInputOption="USER_ENTERED", json=update_body
                )
            )
        except HTTPError as e:
            msg = "Не удалось отправить сроку в таблицу!"
            logger.critical(msg, e)
            raise HTTPError(msg)
        logger.info(settings.SPREADSHEETS_URL.format(spreadsheetid))


def google_sender(
    values: list[list[Any]],
    spreadsheetid: str = settings.SPREADSHEET_ID,
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
