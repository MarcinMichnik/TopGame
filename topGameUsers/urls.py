from django.conf.urls import include
from django.urls import path
from .views import register, profile, UserStatistics
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("profile/", profile, name="profile"),
    path("register/", register, name="register"),
    path("statistics/", UserStatistics.as_view(), name="statistics"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)