# main_forum/views/question_view.py

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from ..models import Question
from ..forms import QuestionForm

class QuestionListView(generic.ListView):
    """ view for displaying a list of questions, this is the main page of the forum."""
    model = Question
    template_name = "questions.html"
    paginate_by = 50

    def get_queryset(self): # get_queryset is a method that returns the queryset that will be used to retrieve the objects that will be displayed in the list view.
        sort_by = self.request.GET.get('sort_by', 'votes')
        if sort_by == 'votes':
            return Question.objects.filter(status=1).order_by('-net_votes', '-created_on')
        return Question.objects.filter(status=1).order_by('-created_on')

    def get_context_data(self, **kwargs): # get_context_data is a method that returns the context data that will be used to render the list view. Context data is a dictionary that contains the data that will be used to render the list view.
        context = super().get_context_data(**kwargs)
        context['sort_by'] = self.request.GET.get('sort_by', 'votes') # get the sort_by parameter from the request and add it to the context
        return context

class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Question
    template_name = "question_delete.html"
    success_url = reverse_lazy('questions')

    def test_func(self): # test_func is a method that is called to check if the user has permission to delete the question. It returns True if the user has permission, and False otherwise.
        question = self.get_object()
        return question.author == self.request.user or self.request.user.is_superuser
