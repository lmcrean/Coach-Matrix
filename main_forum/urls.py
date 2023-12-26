# main_forum/urls.py 
# (called through classroommatrix/urls.py using path("", include("main_forum.urls"), name="main_forum-urls"))

from . import views
from django.urls import path

urlpatterns = [ # url patterns for the blog app here.
    path('index/', views.QuestionList.as_view(), name='index'), # home page
    path('questions/', views.QuestionList.as_view(), name='questions'), # questions page
    path('ask_question/', views.QuestionCreate.as_view(), name='ask_question'), # ask question page
    path('<slug:slug>/', views.QuestionDetail.as_view(), name='question_detail'), # question detail page
    path('upvote/<slug:slug>', views.Upvote.as_view(), name='question_upvote'), # question upvote
    path('downvote/<slug:slug>', views.Downvote.as_view(), name='question_downvote'), # question downvote
    path('question/<int:pk>/delete/', views.QuestionDelete.as_view(), name='question_delete'), # delete question
    path('question/<slug:slug>/update/', views.QuestionUpdate.as_view(), name='question_update'),
      # update question
]