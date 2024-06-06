
from django.urls import path

from . import views

urlpatterns = [
    path("", views.CreatePollView.as_view(), name="index"),
]

