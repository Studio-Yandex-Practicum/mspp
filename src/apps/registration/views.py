from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from . utils import UserData


def rendering(
    request: HttpRequest,
    template_name: str,
    user_data_keys: tuple[str],
) -> HttpResponse:
    field_msg = ""
    if settings.DEBUG:
        field_msg = "Такого поля нет в Контексте"
    context = {}
    for key in user_data_keys:
        context[key] = UserData.data.get(key, field_msg)
    return render(request, template_name, context)


def registration_new_fund(request: HttpRequest) -> HttpResponse:
    template_name = 'registration/registration_new_fund.html'
    user_data_keys = ("age",)
    return rendering(request, template_name, user_data_keys)


def registration_new_user(request: HttpRequest) -> HttpResponse:
    template_name = 'registration/registration_new_user.html'
    user_data_keys = ("age", "region", "city", "fund")
    return rendering(request, template_name, user_data_keys)
