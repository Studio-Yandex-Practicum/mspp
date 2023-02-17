import logging

from django.conf import FORMATTER, LOGGING_FILENAME_BOT, LOGGING_LEVEL

logger = logging.getLogger(__name__)
logger.setLevel(LOGGING_LEVEL)

filelog = logging.FileHandler(LOGGING_FILENAME_BOT)
filelog.setLevel(LOGGING_LEVEL)

console = logging.StreamHandler()
console.setLevel(LOGGING_LEVEL)

filelog.setFormatter(FORMATTER)
console.setFormatter(FORMATTER)
logger.addHandler(filelog)
logger.addHandler(console)
