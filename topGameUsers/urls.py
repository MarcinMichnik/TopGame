from django.conf.urls import include
from django.urls import path
from .views import register, profile
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("profile/", profile, name="profile"),
    path("register/", register, name="register"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)