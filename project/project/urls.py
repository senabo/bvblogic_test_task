"""project URL Configuration """

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


urlpatterns = [
    path("api/v1/api-auth/", include("rest_framework.urls")),
    path(
        "api/v1/oauth2/", include("oauth2_provider.urls", namespace="oauth2_provider")
    ),
    path(
        "api/v1/password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    path("api/v1/", include("accounts.api.urls")),
    path("api/v1/", include("forum.api.urls"))
]

# Generate swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Forum API",
        default_version="v1",
        contact=openapi.Contact(email="senabo33@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path("admin/", admin.site.urls),
    re_path(
        r"^doc(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "api/v1/doc/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "api/v1/redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
