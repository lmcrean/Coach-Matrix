from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from ..models import Question, Answer

class BaseVotingView(LoginRequiredMixin, View):
    model = None
    vote_type = None

    def post(self, request, *args, **kwargs):
        # Adjusted to handle slug correctly
        identifier = kwargs.get('pk') or kwargs.get('slug')
        if 'slug' in kwargs:
            obj = get_object_or_404(self.model, slug=identifier)
        else:
            obj = get_object_or_404(self.model, pk=identifier)

        if obj.author == request.user:
            messages.error(request, "You cannot vote on your own post.")
            return self.get_redirect_url(obj)

        vote_attr = getattr(obj, self.vote_type)
        if vote_attr.filter(id=request.user.id).exists():
            vote_attr.remove(request.user)
            action_msg = "removed"
        else:
            vote_attr.add(request.user)
            action_msg = "added"

        messages.success(request, f"Your vote has been {action_msg}.")
        return self.get_redirect_url(obj)

    def get_redirect_url(self, obj):
        if isinstance(obj, Question):
            return HttpResponseRedirect(reverse('question_detail', args=[obj.slug]))
        elif isinstance(obj, Answer):
            return HttpResponseRedirect(reverse('question_detail', kwargs={'slug': obj.question.slug}))

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])

class QuestionUpvote(BaseVotingView):
    model = Question
    vote_type = 'upvotes'

class QuestionDownvote(BaseVotingView):
    model = Question
    vote_type = 'downvotes'

class AnswerUpvote(BaseVotingView):
    model = Answer
    vote_type = 'upvotes'

    def get_redirect_url(self, obj):
        return redirect('question_detail', slug=obj.question.slug)

class AnswerDownvote(BaseVotingView):
    model = Answer
    vote_type = 'downvotes'

    def get_redirect_url(self, obj):
        return redirect('question_detail', slug=obj.question.slug)
