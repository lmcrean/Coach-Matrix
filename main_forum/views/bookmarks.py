# main_forum/views/bookmarks.py

from django.db import models
from django.db.models import Count, F
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from ..models import Question, Bookmark
from ..forms import AnswerForm, QuestionForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DeleteView, TemplateView, ListView
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from django.contrib import messages
import logging
logger = logging.getLogger(__name__)


class BookmarkedQuestionsList(LoginRequiredMixin, ListView):
    """
    This class will create a view for the user's bookmarked questions. It will display the user's bookmarked questions in a list format that will be displayed in the bookmarked_questions.html template.
    """
    model = Question # should this not be Bookmark?
    template_name = 'bookmarks.html'
    context_object_name = 'bookmarked_question_list'

    def get_queryset(self):
        return Question.objects.filter(bookmarked_by__user=self.request.user)


class CreateBookmark(LoginRequiredMixin, View):
    print('CreateBookmark')
    def post(self, request, *args, **kwargs):
        print('CreateBookmark_post')
        question_id = self.kwargs.get('question_id')
        print('question_id', question_id)
        question = get_object_or_404(Question, id=question_id)
        print('question', question)
        Bookmark.objects.get_or_create(user=request.user, question=question)
        print('Bookmark.objects.get_or_create')
        return HttpResponseRedirect(reverse('question_detail', args=[question.slug]))

class DeleteBookmark(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        question_id = self.kwargs.get('question_id')
        question = get_object_or_404(Question, id=question_id)
        Bookmark.objects.filter(user=request.user, question=question).delete()
        return HttpResponseRedirect(reverse('question_detail', args=[question.slug]))