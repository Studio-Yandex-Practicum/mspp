import logging

# from django.conf import FORMATTER, LOGGING_FILENAME_BOT, LOGGING_LEVEL
from django.conf import settings

logger = logging.getLogger(__name__)
logger.setLevel(settings.LOGGING_LEVEL)

filelog = logging.FileHandler(settings.LOGGING_FILENAME_BOT)
filelog.setLevel(settings.LOGGING_LEVEL)

console = logging.StreamHandler()
console.setLevel(settings.LOGGING_LEVEL)

filelog.setFormatter(settings.FORMATTER)
console.setFormatter(settings.FORMATTER)
logger.addHandler(filelog)
logger.addHandler(console)
