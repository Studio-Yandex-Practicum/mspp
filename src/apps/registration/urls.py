from django.urls import path

from .views import registration_new_fund, registration_new_user

urlpatterns = [
    path("new-fund/<str:age>/", registration_new_fund, name="new_fund"),
    path("new-user/<str:age>/<str:region>/<str:city>/<str:fund>/", registration_new_user, name="new_user"),
]
