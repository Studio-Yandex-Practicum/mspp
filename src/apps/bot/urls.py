from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import BotWebhookView, registration_form

urlpatterns = [
    path("", csrf_exempt(BotWebhookView.as_view()), name="bot_webhook"),
    path("registration/", registration_form, name="registration_form"),
]
