from django.conf.urls import include
from django.urls import path
from .views import register

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("register/", register, name="register"),
]