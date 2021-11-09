from django.urls import path, re_path

from scouts_auth.views import (
    CurrentUserView,
    OIDCAuthCodeView,
    OIDCRefreshView,
)

urlpatterns = [
    # The infamous "me" call
    path("auth/me/", CurrentUserView.as_view(), name="me"),
    # Authenticate with OIDC
    path("oidc/token/", OIDCAuthCodeView.as_view(), name="token"),
    # Refresh the OIDC authentication
    path("oidc/refresh/", OIDCRefreshView.as_view(), name="refresh"),
    # path("oidc/", include("mozilla_django_oidc.urls")),
]
