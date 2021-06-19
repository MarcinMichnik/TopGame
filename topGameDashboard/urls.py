from django.conf.urls import include, url
from django.urls import path
from .views import dashboard

urlpatterns = [
    path("", dashboard, name="dashboard"),
]