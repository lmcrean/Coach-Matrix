# users/urls.py

from django.urls import path
from .views import (
    home, custom_login_view, logout_view, questions_view, custom_signup_view, change_password, profile_view, profile_update
    )

urlpatterns = [
    path('', home, name='home'),  # Root URL for home page with login/signup forms
    path('login/', custom_login_view, name='custom_login'),
    path('signup/', custom_signup_view, name='custom_signup'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='my_profile')
]