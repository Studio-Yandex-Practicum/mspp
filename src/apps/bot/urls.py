from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import BotWebhookView

urlpatterns = [
    path("", csrf_exempt(BotWebhookView.as_view()), name="bot_webhook"),
]
