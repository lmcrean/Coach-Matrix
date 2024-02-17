# users/urls.py

from django.urls import path
from .views import home, custom_login_view, logout_view, questions_view

urlpatterns = [
    path('', home, name='home'),  # Home page with login form
    path('login/', custom_login_view, name='custom_login'),  # Endpoint for processing login form
    path('logout/', logout_view, name='logout'),  # Logout endpoint
    path('questions/', questions_view, name='questions'),  # Questions page
]