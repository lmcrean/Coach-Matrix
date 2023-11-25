from . import views
from django.urls import path


urlpatterns = [ # url patterns for the blog app here.
    path('index/', views.PostList.as_view(), name='index'), # home page
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'), # post detail page
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'), # post like
    path('questions/', views.PostList.as_view(), name='questions'), # questions page
]