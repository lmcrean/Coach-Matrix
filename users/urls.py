#users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('login/', views.custom_login_view, name='custom_login'),  # Custom login page
    path('questions/', views.questions_view, name='questions'),  # Questions page
    path('logout/', views.logout_view, name='logout'),  # Logout view
]