import logging
import sys
from pathlib import Path

import environ
from django.core.management.utils import get_random_secret_key

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "apps"))

env = environ.Env()

SECRET_KEY = env("SECRET_KEY", default=get_random_secret_key())

DEBUG = env.bool("DEBUG", default=True)

ALLOWED_HOSTS = list(map(str.strip, env.list("ALLOWED_HOSTS", default=["*"])))
CSRF_TRUSTED_ORIGINS = list(
    map(str.strip, env.list("CSRF_TRUSTED_ORIGINS", default=["http://127.0.0.1", "http://localhost"]))
)

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


# Use PostgreSQL
# ------------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB", default="mspp"),
        "USER": env("POSTGRES_USER", default="mspp"),
        "PASSWORD": env("POSTGRES_PASSWORD", default="pg_password"),
        "HOST": env("POSTGRES_HOST", default="postgres"),
        "PORT": env("POSTGRES_PORT", default="5432"),
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
LOGGING_LEVEL = env("LOGGING_LEVEL", default="DEBUG")
LOG_DIR = BASE_DIR / "src/.logs"
LOGGING_FILENAME = LOG_DIR / "system.log"
LOGGING_FILENAME_BOT = LOG_DIR / "bot.log"
FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
TELEGRAM_TOKEN = env("TELEGRAM_TOKEN")
WEBHOOK_MODE = env.bool("WEBHOOK_MODE", default=False)
WEBHOOK_URL = env("WEBHOOK_URL", default=environ.Env.NOTSET if WEBHOOK_MODE else "")

# Google
CREDENTIALS_TYPE = env("CREDENTIALS_TYPE", default="env")
SPREADSHEETS_URL = "https://docs.google.com/spreadsheets/d/{0}"
SPREADSHEET_ID = env("SPREADSHEET_ID", default="_")
SCOPES = ("https://www.googleapis.com/auth/spreadsheets",)

EMAIL_USER = env("EMAIL", default="example@mail.com")
PRIVATE_KEY = env.str("PRIVATE_KEY", multiline=True, default="_")
ENV_INFO = {
    "project_id": env("PROJECT_ID", default="_"),
    "private_key_id": env("PRIVATE_KEY_ID", default="_"),
    "private_key": PRIVATE_KEY,
    "client_email": env("CLIENT_EMAIL", default="_"),
    "client_id": env("CLIENT_ID", default="_"),
    "client_x509_cert_url": env("CLIENT_X509_CERT_URL", default="_"),
}

logging.basicConfig(
    level=LOGGING_LEVEL,
    filename=LOGGING_FILENAME,
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s",
)
