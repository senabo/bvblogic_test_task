from django.urls import path
from .views import CreateProfileView, UpdateProfileView

app_name = "accounts"


urlpatterns = [
    path("user/registration", CreateProfileView.as_view(), name="create_user"),
    path(
        "user/<slug:username>/",
        UpdateProfileView.as_view(),
        name="update_user_profile",
    ),
]
