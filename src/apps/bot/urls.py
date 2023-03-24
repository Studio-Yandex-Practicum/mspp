from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import (
    BotWebhookView,
    registration_new_fund,
    registration_new_user,
)

PREFIX = "registration/"


urlpatterns = [
    path("",
         csrf_exempt(BotWebhookView.as_view()),
         name="bot_webhook"),
    path(f"{PREFIX}new-fund/",
         registration_new_fund,
         name="registration_new_fund"),
    path(f"{PREFIX}new-user/",
         registration_new_user,
         name="registration_new_user"),
]
