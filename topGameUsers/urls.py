from django.conf.urls import include
from django.urls import path
from .views import Register, Profile, UserStatistics
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("profile/", Profile.as_view(), name="profile"),
    path("register/", Register.as_view(), name="register"),
    path("statistics/", UserStatistics.as_view(), name="statistics"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)