from django.urls import path
from . import views

urlpatterns = [
    path("github/webhook/", views.github_webhook),
]