import asyncio
from typing import Any

from django.conf import settings

from .service import send


def google_sender(
    values: list[list[Any]],
    spreadsheetid: str = settings.SPREADSHEET_ID,
) -> None:
    """Отправляет переданные данные в Google таблицы.

    Args:
        table_values (list[list[Any]]): Значения колонок
        spreadsheetid (str): ID Google таблицы. Defaults to settings.SPREADSHEET_ID.

    Raises:
        APIConnectFailed: Не удалось подключиться к Google API
        SendFailed: Не удалось отправить сроку в таблицу
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.get_event_loop().run_until_complete(send(spreadsheetid, values))
