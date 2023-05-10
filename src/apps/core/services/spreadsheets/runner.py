import asyncio
from typing import Any

from django.conf import settings

from .spreadsheets import send, set_user_permissions


async def send_to_google_sheets(
    table_values: list[list[Any]],
    spreadsheetid: str = settings.SPREADSHEET_ID,
) -> None:
    """Отправляет переданные данные в Google таблицы.

    Args:
        table_values (list[list[Any]]): Значения колонок
        spreadsheetid (str): ID Google таблицы. Defaults to settings.SPREADSHEET_ID.

    Raises:
        HTTPError: Не удалось отправить сроку в таблицу
    """
    task_1 = asyncio.create_task(set_user_permissions(spreadsheetid))
    task_2 = asyncio.create_task(send(table_values, spreadsheetid))
    await task_1
    await task_2
