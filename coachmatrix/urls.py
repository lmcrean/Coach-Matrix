# coachmatrix/urls.py is the main URL configuration for the project. It is the first thing that is read when the server is started. It is responsible for routing requests to the appropriate app.

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),  # Admin page
    path('login/', include('users.urls')),  # Login page handled by users app
    path('', include('main_forum.urls')),  # Include the main_forum app URLs
    path('accounts/', include('allauth.urls')),  # Include the allauth app URLs
]