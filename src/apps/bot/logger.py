import os
import logging
from logging.handlers import TimedRotatingFileHandler

from django.conf import settings

def create_log_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

create_log_directory(settings.LOG_DIR)
logger = logging.getLogger(__name__)
logger.setLevel(settings.LOGGING_LEVEL)

filelog = TimedRotatingFileHandler(settings.LOGGING_FILENAME_BOT)
filelog.setLevel(settings.LOGGING_LEVEL)

console = logging.StreamHandler()
console.setLevel(settings.LOGGING_LEVEL)

filelog.setFormatter(settings.FORMATTER)
console.setFormatter(settings.FORMATTER)
logger.addHandler(filelog)
logger.addHandler(console)
