# main_forum/urls.py 
# (called through coachmatrix/urls.py using path("", include("main_forum.urls"), name="main_forum-urls"))

from . import views
from django.urls import path

urlpatterns = [ # url patterns for the blog app here.
    path('index/', views.QuestionList.as_view(), name='index'), # home page
    path('questions/', views.QuestionList.as_view(), name='questions'), # questions page
    path('ask_question/', views.QuestionCreate.as_view(), name='ask_question'), # ask question page
    path('profile/', views.ProfileView.as_view(), name='my_profile'),  # My Profile page
    path('bookmarked/', views.BookmarkedQuestionsList.as_view(), name='bookmarked_questions'),  # Bookmarked Questions page

    path('<slug:slug>/', views.QuestionDetail.as_view(), name='question_detail'), # question detail page
    
    path('upvote/<slug:slug>', views.Upvote.as_view(), name='question_upvote'), # question upvote
    path('downvote/<slug:slug>', views.Downvote.as_view(), name='question_downvote'), # question downvote
    path('questions/<slug:slug>/upvote/', views.QuestionUpvoteFromList.as_view(), name='question_upvote_from_list'), # question upvote from list
    path('questions/<slug:slug>/downvote/', views.QuestionDownvoteFromList.as_view(), name='question_downvote_from_list'), # question downvote from list
    path('question/<int:pk>/delete/', views.QuestionDelete.as_view(), name='question_delete'), # delete question
    path('question/<slug:slug>/update/', views.QuestionUpdate.as_view(), name='question_update'), # update question
    path('answer/<slug:slug>/update/', views.AnswerUpdate.as_view(), name='answer_update'),  # Update answer
    path('answer/<slug:slug>/delete/', views.AnswerDelete.as_view(), name='answer_delete'), # Delete answer
    path('answer/<int:pk>/upvote/', views.AnswerUpvote.as_view(), name='answer_upvote'), # Answer upvote
    path('answer/<int:pk>/downvote/', views.AnswerDownvote.as_view(), name='answer_downvote'), # Answer downvote
]