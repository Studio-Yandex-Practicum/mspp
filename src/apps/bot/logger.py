import logging
import os
from logging.handlers import TimedRotatingFileHandler

from src.config.settings import LOG_DIR

FORMATTER = "%(asctime)s\t%(levelname)s\t%(filename)s:%(lineno)d\t%(message)s"


def create_log_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def add_handler(path_name):
    handler = TimedRotatingFileHandler(
        f"{LOG_DIR}/{path_name}", when="midnight", interval=1, encoding="utf-8", backupCount=14
    )
    formatter = logging.Formatter(FORMATTER)
    handler.setFormatter(formatter)
    return handler


def bot_logging():

    bot_logger = logging.getLogger("telegram")
    bot_logger.setLevel(logging.INFO)
    bot_handler = add_handler("bot_logs.txt")
    bot_logger.addHandler(bot_handler)

    return bot_logger


#
# logger = logging.getLogger(__name__)
# logger.setLevel(settings.LOGGING_LEVEL)
#
# filelog = logging.FileHandler(settings.LOGGING_FILENAME_BOT)
# filelog.setLevel(settings.LOGGING_LEVEL)
#
# console = logging.StreamHandler()
# console.setLevel(settings.LOGGING_LEVEL)
#
# filelog.setFormatter(settings.FORMATTER)
# console.setFormatter(settings.FORMATTER)
# logger.addHandler(filelog)
# logger.addHandler(console)


bot_logger = bot_logging()
