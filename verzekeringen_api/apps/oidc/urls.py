from django.urls import path
from .api.views import AuthCodeView, RefreshView

urlpatterns = [
    path("token/", AuthCodeView.as_view()),
    path("refresh/", RefreshView.as_view()),
]
