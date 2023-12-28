#users/urls.py

from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name='home'), # home page
    path("questions/", views.logintoquestions, name='questions'), # questions page
    path("accounts/", include("allauth.urls")),
    path("logout", views.logout_view)
]