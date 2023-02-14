import logging

from django.conf import FORMATTER, LOG_FILE_BOT, LOGGING_LEVEL

logger = logging.getLogger(__name__)
logger.setLevel(LOGGING_LEVEL)

filelog = logging.FileHandler(LOG_FILE_BOT)
filelog.setLevel(LOGGING_LEVEL)

console = logging.StreamHandler()
console.setLevel(LOGGING_LEVEL)

filelog.setFormatter(FORMATTER)
console.setFormatter(FORMATTER)
logger.addHandler(filelog)
logger.addHandler(console)
