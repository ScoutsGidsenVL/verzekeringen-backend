from django.urls import path
from .api.views import CurrentUserView

urlpatterns = [
    path("me/", CurrentUserView.as_view()),
]
