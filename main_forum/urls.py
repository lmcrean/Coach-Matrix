# main_forum/urls.py 
# (called through coachmatrix/urls.py using path("", include("main_forum.urls"), name="main_forum-urls"))

from .views.answers import QuestionDetail, AnswerUpdate, AnswerDelete
from .views.questions import QuestionList, QuestionCreate, QuestionUpdate, QuestionDelete
from .views.voting import Upvote, Downvote, QuestionUpvoteFromList, QuestionDownvoteFromList, AnswerUpvote, AnswerDownvote
from .views.profile import ProfileView
from .views.bookmarks import BookmarkedQuestionsList
from django.urls import path

urlpatterns = [ # url patterns for the blog app here.
    path('index/', QuestionList.as_view(), name='index'), # home page
    path('questions/', QuestionList.as_view(), name='questions'), # questions page
    path('ask_question/', QuestionCreate.as_view(), name='ask_question'), # ask question page
    path('profile/', ProfileView.as_view(), name='my_profile'),  # My Profile page
    path('bookmarked/', BookmarkedQuestionsList.as_view(), name='bookmarked_questions'),  # Bookmarked Questions page

    path('<slug:slug>/', QuestionDetail.as_view(), name='question_detail'), # question detail page
    
    path('upvote/<slug:slug>', Upvote.as_view(), name='question_upvote'), # question upvote
    path('downvote/<slug:slug>', Downvote.as_view(), name='question_downvote'), # question downvote
    path('questions/<slug:slug>/upvote/', QuestionUpvoteFromList.as_view(), name='question_upvote_from_list'), # question upvote from list
    path('questions/<slug:slug>/downvote/', QuestionDownvoteFromList.as_view(), name='question_downvote_from_list'), # question downvote from list
    path('question/<int:pk>/delete/', QuestionDelete.as_view(), name='question_delete'), # delete question
    path('question/<slug:slug>/update/', QuestionUpdate.as_view(), name='question_update'), # update question
    path('answer/<slug:slug>/update/', AnswerUpdate.as_view(), name='answer_update'),  # Update answer
    path('answer/<slug:slug>/delete/', AnswerDelete.as_view(), name='answer_delete'), # Delete answer
    path('answer/<int:pk>/upvote/', AnswerUpvote.as_view(), name='answer_upvote'), # Answer upvote
    path('answer/<int:pk>/downvote/', AnswerDownvote.as_view(), name='answer_downvote'), # Answer downvote
]