from django.conf.urls import include
from django.urls import path
from .views import register, profile

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("profile/", profile, name="profile"),
    path("register/", register, name="register"),
]