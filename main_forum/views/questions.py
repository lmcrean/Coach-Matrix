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

class QuestionList(generic.ListView):
    model = Question
    template_name = "questions.html"
    paginate_by = 50  # Display 50 questions per page

    def get_queryset(self): # This function will get the queryset for the view. A queryset is a list of objects of a given model. In this case, we are getting a list of questions.
        sort_by = self.request.GET.get('sort_by', 'votes')  # Default sort by votes

        if sort_by == 'votes':
            return Question.objects.filter(status=1).order_by('-net_votes', '-created_on')
        else:
            return Question.objects.filter(status=1).order_by('-created_on')

    def get_context_data(self, **kwargs): # This function will get the context data for the view. Context data is a dictionary of values that are passed to the template. In this case, we are passing the sort_by parameter to the template. This function will be called when the view is rendered.
        context = super().get_context_data(**kwargs) # Call the super() method to get the context data from the parent class. The context data in this case is the list of questions.
        context['sort_by'] = self.request.GET.get('sort_by', 'votes') # Get the sort_by parameter from the URL. If it doesn't exist, default to 'votes'.
        return context # Return the context data


class QuestionCreate(generic.CreateView): # this class will create a question
    """
    Form for asking a question. The user can enter a subject line and the main body of the question. They can also tag the question.

    This class should help create an instance of the Question model. It will also use the QuestionForm class to create the form.

    *args and *kwargs are used to pass a variable number of arguments to a function.
    """
    model = Question
    form_class = QuestionForm  # Use the custom form class
    template_name = "ask_question.html"

    def form_valid(self, form):
        # Assign the current user as the author of the question
        form.instance.author = self.request.user
        form.instance.status = 1
        
        # save the form instance before adding many-to-many relations
        response = super(QuestionCreate, self).form_valid(form)

        # Get the tags data from the form, process it, and add the tags to the instance
        tags = form.cleaned_data.get('tags', '')
        if tags:
            tag_list = [tag.strip() for tag in tags.split(' ')]
            for tag_name in tag_list:
                tag, created = TeachingStandardTag.objects.get_or_create(name=tag_name)
                self.object.standard.add(tag)  # Assuming `standard` is a many-to-many field in your Question model for tags

        if form.is_valid():
            # process and save the form
            question = form.save(commit=False)
        else:
            print(form.errors) 

        return response
    
    def get_success_url(self):
        # Redirect to the 'questions' page after form submission
        return reverse_lazy('questions')
    
class QuestionUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'ask_question.html'  # Reuse the ask_question template or create a specific one for updates

    def get_object(self):
        # Override get_object to ensure the user can only edit their own question
        question = get_object_or_404(Question, slug=self.kwargs['slug'], author=self.request.user)
        return question

    def get_queryset(self):
        return Question.objects.filter(slug=self.kwargs['slug'], author=self.request.user)

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def form_valid(self, form):
        # Save the form first without committing to get the instance
        question = form.save(commit=False)
        # Update the slug and title
        question.title = form.cleaned_data['subject']
        question.slug = slugify(form.cleaned_data['subject'])
        # Save the instance
        question.save()
        # Now save many-to-many data
        form.save_m2m()
        # Use the updated slug for redirection
        return HttpResponseRedirect(reverse('question_detail', kwargs={'slug': question.slug}))

    def get_success_url(self):
        # Redirect to the updated question's detail page or some success page
        question = self.get_object()
        return reverse_lazy('question_detail', kwargs={'slug': self.object.slug})
    
    
class QuestionDelete(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    """
    This class will delete a question.

    Only the author of a question can delete it, or an admin/ superuser.

    LoginRequiredMixin: Ensures that only authenticated users can access this view.
    UserPassesTestMixin: Defines a test function (test_func) that must return True for the view to proceed. In this case, it checks if the current user is the author of the post or an admin/superuser.
    """
    model = Question
    template_name = "question_delete.html"
    success_url = reverse_lazy('questions')  # Redirect to the questions list after deletion

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.author or self.request.user.is_superuser:
            return True
        return False
