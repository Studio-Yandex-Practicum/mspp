import logging

from django.conf import settings

logger = logging.getLogger(__name__)
logger.setLevel(settings.LOGGING_LEVEL)

formatter = logging.Formatter("%(levelname)s - %(message)s")
handler = logging.StreamHandler()

handler.setFormatter(formatter)
logger.addHandler(handler)
