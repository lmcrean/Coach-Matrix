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
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
import logging
logger = logging.getLogger(__name__)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'my_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def profile_view(request):
    user = request.user
    context = {
        'username': user.username,
        'email': user.email,
        'is_oauth': False
    }

    # Check if the user has logged in using social accounts
    social_accounts = SocialAccount.objects.filter(user=user)
    if social_accounts.exists():
        context['is_oauth'] = True
        context['provider'] = social_accounts.first().provider

    return render(request, 'my_profile.html', context)