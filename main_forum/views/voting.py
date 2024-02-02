from django.db import models
from django.db.models import Count, F
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from ..models import Question, Tag, Answer
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


class Upvote(View):
    """
    This class will handle upvoting a question from question_detail view. If the user has already upvoted the question, it will remove the upvote. If the user has not already upvoted the question, it will add the upvote.
    """
    def post(self, request, slug, *args, **kwargs):
        question = get_object_or_404(Question, slug=slug)
        if question.author == request.user:
            messages.error(request, "You cannot upvote your own question.")
            return HttpResponseRedirect(reverse('question_detail', args=[slug]))

        if question.upvotes.filter(id=request.user.id).exists():
            question.upvotes.remove(request.user)
        else:
            question.upvotes.add(request.user)
        return HttpResponseRedirect(reverse('question_detail', args=[slug]))
        pass

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])


class Downvote(View):
    """
    This class will handle downvoting a question from question_detail view. If the user has already downvoted the question, it will remove the downvote. If the user has not already downvoted the question, it will add the downvote.
    """
    def post(self, request, slug, *args, **kwargs):
        question = get_object_or_404(Question, slug=slug)
        if question.author == request.user:
            messages.error(request, "You cannot downvote your own question.")
            return HttpResponseRedirect(reverse('question_detail', args=[slug]))

        if question.downvotes.filter(id=request.user.id).exists():
            question.downvotes.remove(request.user)
        else:
            question.downvotes.add(request.user)
        return HttpResponseRedirect(reverse('question_detail', args=[slug]))
        pass

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])

class QuestionUpvoteFromList(LoginRequiredMixin, View):
    def get(self, request, slug, *args, **kwargs):
        return HttpResponseRedirect(reverse('questions'))

    def post(self, request, slug, *args, **kwargs):
        question = get_object_or_404(Question, slug=slug)
        if question.author == request.user:
            messages.error(request, "You cannot upvote your own question.")
        else:
            if question.upvotes.filter(id=request.user.id).exists():
                question.upvotes.remove(request.user)
                messages.success(request, "Your upvote has been removed.")
                question.save()  # Save to update net_votes
            else:
                question.upvotes.add(request.user)
                messages.success(request, "You have upvoted this question.")
                question.save()  # Save to update net_votes

        # Redirect back to the questions list
        return HttpResponseRedirect(reverse('questions'))

class QuestionDownvoteFromList(LoginRequiredMixin, View):
    def get(self, request, slug, *args, **kwargs):
        return HttpResponseRedirect(reverse('questions'))

    def post(self, request, slug, *args, **kwargs):
        question = get_object_or_404(Question, slug=slug)
        if question.author == request.user:
            messages.error(request, "You cannot downvote your own question.")
        else:
            if question.downvotes.filter(id=request.user.id).exists():
                question.downvotes.remove(request.user)
                messages.success(request, "Your downvote has been removed.")
            else:
                question.downvotes.add(request.user)
                messages.success(request, "You have downvoted this question.")

        # Redirect back to the questions list
        return HttpResponseRedirect(reverse('questions'))


class AnswerUpvote(LoginRequiredMixin, View):
    def post(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        if request.user == answer.author:
            messages.error(request, "You cannot vote on your own answer.")
        else:
            if answer.upvotes.filter(id=request.user.id).exists():
                answer.upvotes.remove(request.user)
                messages.success(request, "Your upvote has been removed.")
            else:
                answer.upvotes.add(request.user)
                messages.success(request, "You have upvoted this answer.")
        return redirect('question_detail', slug=answer.question.slug)

class AnswerDownvote(LoginRequiredMixin, View):
    def post(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        if request.user == answer.author:
            messages.error(request, "You cannot vote on your own answer.")
        else:
            if answer.downvotes.filter(id=request.user.id).exists():
                answer.downvotes.remove(request.user)
                messages.success(request, "Your downvote has been removed.")
            else:
                answer.downvotes.add(request.user)
                messages.success(request, "You have downvoted this answer.")
        return redirect('question_detail', slug=answer.question.slug)
