from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("accounts/", include("allauth.urls")),
    path("logout", views.logout_view)
]