# users/urls.py

from django.urls import path
from .views import (
    home, custom_login_view, custom_signup_view, logout_view, ProfileView, delete_profile
    )

urlpatterns = [
    path('', home, name='home'),  # Root URL for home page with login/signup forms
    path('login/', custom_login_view, name='custom_login'),
    path('signup/', custom_signup_view, name='custom_signup'),
    path('logout/', logout_view, name='logout'),
    path('profile/', ProfileView.as_view(), name='my_profile'),
    path('delete_profile/', delete_profile, name='delete_profile')
]