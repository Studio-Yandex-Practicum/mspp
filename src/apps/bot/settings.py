import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_MODE = os.getenv("WEBHOOK_MODE", "False").lower() == "true"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
