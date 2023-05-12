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
    map(str.strip, env.list("CSRF_TRUSTED_ORIGINS", default=["https://127.0.0.1", "https://localhost"]))
)

PERSISTANCE_DIR = BASE_DIR / "persistance_data"
PERSISTANCE_PATH = PERSISTANCE_DIR / "persistance_file"
Path.mkdir(PERSISTANCE_DIR, exist_ok=True)

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
    "registration",
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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB", default="mspp"),
        "USER": env("POSTGRES_USER", default="mspp"),
        "PASSWORD": env("POSTGRES_PASSWORD", default="pg_password"),
        "HOST": env("POSTGRES_HOST", default="localhost"),
        "PORT": env("POSTGRES_PORT", default="9999"),
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

LOG_DIR = BASE_DIR / "logs"
Path.mkdir(LOG_DIR, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "common_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/app.log",
            "backupCount": 10,
            "formatter": "verbose",
        }
    },
    "loggers": {
        "": {
            "level": "WARNING",
            "handlers": ["common_file"],
        }
    },
    "formatters": {
        "verbose": {
            "format": "{name} {levelname} {asctime} {process:d} {message}",
            "style": "{",
        }
    },
}

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TELEGRAM_TOKEN = env("TELEGRAM_TOKEN")
WEBHOOK_MODE = env.bool("WEBHOOK_MODE", default=False)
WEBHOOK_URL = env("WEBHOOK_URL", default=environ.Env.NOTSET if WEBHOOK_MODE else "")

# Google Spreadsheets Variables
CREDENTIALS_TYPE = env("CREDENTIALS_TYPE", default="env")
SPREADSHEETS_URL = "https://docs.google.com/spreadsheets/d/{0}"
SPREADSHEET_ID_NEW_FUND = env("SPREADSHEET_ID_NEW_FUND", default="_")
SPREADSHEET_ID_VOLUNTEER = env("SPREADSHEET_ID_VOLUNTEER", default="_")

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

GOOGLE_FORM_URL = "https://docs.google.com/forms/u/0/d/e/{0}/formResponse"
GOOGLE_FORM_ID = "1FAIpQLSdyfRyOfDfB3X75eEQoTOgBA8bGfe68Lthy-03EdwnnE_U9QA"
GOOGLE_FORM_FIELDS = {
    "surname": "50190039",
    "first_name": "1395634080",
    "patronymic": "864793007",
    "age": "905514263",
    "country": "16057190",
    "region": "1475908288",
    "city": "969207866",
    "job": "1848219250",
    "email": "894713360",
    "phone": "1686121456",
    "fund_name": "802736698",
}

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
