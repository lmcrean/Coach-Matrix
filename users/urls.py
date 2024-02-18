# users/urls.py

from django.urls import path
from .views import (
    home, custom_login_view, logout_view, questions_view, custom_signup_view, change_password, profile_view
    )

urlpatterns = [
    path('', home, name='home'),  # Root URL for home page with login/signup forms
    path('login/', custom_login_view, name='custom_login'),
    path('signup/', custom_signup_view, name='custom_signup'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='my_profile'),
    path('profile/', profile_view, name='profile_update'),
    path('profile/', change_password, name='change_password'),
    path('profile/', profile_view, name='change_password_done'),
]