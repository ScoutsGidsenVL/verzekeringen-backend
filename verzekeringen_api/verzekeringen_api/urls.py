"""verzekeringen_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi

# Open api schema
schema_view = get_schema_view(
    openapi.Info(
        title="Scouts verzekeringen API",
        default_version="v1",
        description="This is the api documentation for the Scouts verzekeringen API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("api/", include("apps.insurances.urls")),
    path("api/", include("apps.members.urls")),
    path("api/", include("apps.equipment.urls")),
    path("api/", include("apps.locations.urls")),
    path("api/", include("apps.info.urls")),
    path("api/", include("inuits.files.urls")),
    path("api/auth/", include("apps.scouts_auth.urls")),
    path("api/oidc/", include("apps.oidc.urls")),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("api/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]
