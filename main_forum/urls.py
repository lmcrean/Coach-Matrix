from django.urls import path
from .views import (
    QuestionListView, QuestionCreateView, QuestionUpdateView, QuestionDeleteView,
    QuestionDetail, AnswerUpdate, AnswerDelete,
    ProfileView, BookmarkedQuestionsList,
    QuestionUpvote, QuestionDownvote, AnswerUpvote, AnswerDownvote
)

urlpatterns = [
    path('index/', QuestionListView.as_view(), name='index'),
    path('questions/', QuestionListView.as_view(), name='questions'),
    path('ask_question/', QuestionCreateView.as_view(), name='ask_question'),
    path('profile/', ProfileView.as_view(), name='my_profile'),
    path('bookmarked/', BookmarkedQuestionsList.as_view(), name='bookmarked_questions'),
    path('<slug:slug>/', QuestionDetail.as_view(), name='question_detail'),
    path('question/<slug:slug>/upvote/', QuestionUpvote.as_view(), name='question_upvote'),
    path('question/<slug:slug>/downvote/', QuestionDownvote.as_view(), name='question_downvote'),
    path('question/<slug:slug>/update/', QuestionUpdateView.as_view(), name='question_update'),
    path('question/<slug:slug>/delete/', QuestionDeleteView.as_view(), name='question_delete'),
    path('answer/<int:pk>/update/', AnswerUpdate.as_view(), name='answer_update'),
    path('answer/<int:pk>/delete/', AnswerDelete.as_view(), name='answer_delete'),
    path('answer/<int:pk>/upvote/', AnswerUpvote.as_view(), name='answer_upvote'),
    path('answer/<int:pk>/downvote/', AnswerDownvote.as_view(), name='answer_downvote'),
]
