import logging
import os
import sys
import uuid
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "apps"))


if os.path.exists(BASE_DIR.parent / ".env"):
    dotenv_path = Path(BASE_DIR.parent / ".env")
else:
    dotenv_path = Path(BASE_DIR.parent / ".env_local")

env = environ.Env()
with dotenv_path.open() as file:
    environ.Env.read_env(file)
if env("SECRET_KEY"):
    SECRET_KEY = env("SECRET_KEY")
else:
    SECRET_KEY = str(uuid.uuid1())

DEBUG = env.bool("DEBUG", default=True)

ALLOWED_HOSTS = list(map(str.strip, env.list("ALLOWED_HOSTS", default=["*"])))

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "mptt",
    "bot.apps.BotConfig",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


DB_DIR = BASE_DIR / ".data"
DB_DIR.mkdir(exist_ok=True)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": DB_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Telegram
LOGGING_LEVEL = logging.env("LOGGING_LEVEL")
FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FILE_BOT = ".data/bot.log"
TELEGRAM_TOKEN = env("TELEGRAM_TOKEN")
WEBHOOK_MODE = env.bool("WEBHOOK_MODE", default=False)
WEBHOOK_URL = env("WEBHOOK_URL", default=environ.Env.NOTSET if WEBHOOK_MODE else "")

# Google
LOGGING_LEVEL = env("LOGGING_LEVEL")
CREDENTIALS_TYPE = env("CREDENTIALS_TYPE")
SPREADSHEETS_URL = "https://docs.google.com/spreadsheets/d/{0}"
SPREADSHEET_ID = env("SPREADSHEET_ID")
SCOPES = ("https://www.googleapis.com/auth/spreadsheets",)

EMAIL_USER = env("EMAIL")

logging.basicConfig(
    level=logging.LOGGING_LEVEL,
    filename=".data/system.log",
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s",
)

match CREDENTIALS_TYPE:
    case "json":
        JSON_INFO = env("CREDENTIALS_JSON_PATH")
    case "env":
        PRIVATE_KEY = env.str("PRIVATE_KEY", multiline=True)
        ENV_INFO = {
            "project_id": env("PROJECT_ID"),
            "private_key_id": env("PRIVATE_KEY_ID"),
            "private_key": PRIVATE_KEY,
            "client_email": env("CLIENT_EMAIL"),
            "client_id": env("CLIENT_ID"),
            "client_x509_cert_url": env("CLIENT_X509_CERT_URL"),
        }
