from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def registration_new_fund(request: HttpRequest, age: str) -> HttpResponse:
    template_name = "registration/registration_new_fund.html"
    context = {
        "age": age,
    }
    return render(request, template_name, context)


def registration_new_user(
    request: HttpRequest,
    age: str,
    region: str,
    city: str,
    fund: str,
) -> HttpResponse:
    template_name = "registration/registration_new_user.html"
    context = {
        "age": age,
        "region": region,
        "city": city,
        "fund": fund,
    }
    return render(request, template_name, context)
