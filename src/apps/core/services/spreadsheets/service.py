from typing import Any

from aiogoogle import Aiogoogle
from django.conf import settings

from .auth import creds
from .exceptions import APIConnectFailed, SendFailed
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
        APIConnectFailed: Не удалось подключиться к Google API
        SendFailed: Не удалось отправить сроку в таблицу
    """
    async with Aiogoogle(service_account_creds=creds) as aiogoogle:
        try:
            service = await aiogoogle.discover("sheets", "v4")
        except Exception as e:
            logger.critical("Не удалось подключиться к Google API!", e)
            raise APIConnectFailed
        range = f"1:{len(table_values)}"

        update_body = {"majorDimension": "COLUMNS", "values": table_values}
        try:
            await aiogoogle.as_service_account(
                service.spreadsheets.values.append(
                    spreadsheetId=spreadsheetid, range=range, valueInputOption="USER_ENTERED", json=update_body
                )
            )
        except Exception as e:
            logger.critical("Не удалось отправить сроку в таблицу!", e)
            raise SendFailed
        logger.info(settings.SPREADSHEETS_URL.format(spreadsheetid))
