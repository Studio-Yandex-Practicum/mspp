from django.urls import path

from .views import (
    registration_new_fund,
    registration_new_user,
)


urlpatterns = [
    path("new-fund/",
         registration_new_fund,
         name="registration_new_fund"),
    path("new-user/",
         registration_new_user,
         name="registration_new_user"),
]
