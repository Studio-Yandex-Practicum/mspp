from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def registration_new_fund(request: HttpRequest) -> HttpResponse:
    template_name = "registration/registration_new_fund.html"
    if request.method == "GET":
        age = request.GET.get("age")
    context = {
        "age": age,
    }
    return render(request, template_name, context)


def registration_new_user(request: HttpRequest) -> HttpResponse:
    template_name = "registration/registration_new_user.html"

    if request.method == "GET":
        age = request.GET.get("age")
        region = request.GET.get("region")
        city = request.GET.get("city")
        fund = request.GET.get("fund")

    context = {
        "age": age,
        "region": region,
        "city": city,
        "fund": fund,
    }
    return render(request, template_name, context)
