from django.conf.urls import include
from django.urls import path
from .views import MadhexView

urlpatterns = [
    path("play/", MadhexView.as_view(), name="madhex-play"),
]