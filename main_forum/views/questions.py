from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from ..models import Question, Tag
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

class QuestionCreateView(LoginRequiredMixin, generic.CreateView):
    """ view for creating a new question."""
    model = Question
    form_class = QuestionForm
    template_name = "ask_question.html"

    def form_valid(self, form): 
        form.instance.author = self.request.user # set the author of the question to the current user
        form.instance.status = 1 # set the status of the question to 1, which means that the question is published
        response = super().form_valid(form) # call the form_valid method of the parent class. Super() is used to call the method of the parent class.
        self.handle_tags(form) # call the handle_tags method to handle the tags
        return response

    # def handle_tags(self, form):
    #     tags = form.cleaned_data.get('tags', '')
    #     if tags:
    #         tag_list = [Tag.objects.get_or_create(name=tag.strip())[0] for tag in tags.split(' ')]
    #         self.object.tags.set(tag_list)

    def get_success_url(self):
        return reverse_lazy('questions')

class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'ask_question.html'
    context_object_name = 'question' # context_object_name is a variable that is used to specify the name of the variable that will be used to access the object in the template.

    def test_func(self): # test_func is a method that is called to check if the user has permission to update the question. It returns True if the user has permission, and False otherwise.
        return self.get_object().author == self.request.user or self.request.user.is_superuser

    def form_valid(self, form): # form_valid is a method that is called when the form is valid. It is used to save the form data to the database.
        form.instance.slug = slugify(form.cleaned_data.get('subject', '')) # set the slug of the question to the slugified subject
        response = super().form_valid(form) # call the form_valid method of the parent class. Super() is used to call the method of the parent class.
        return response

    def get_success_url(self):
        return reverse_lazy('question_detail', kwargs={'slug': self.object.slug})

class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Question
    template_name = "question_delete.html"
    success_url = reverse_lazy('questions')

    def test_func(self): # test_func is a method that is called to check if the user has permission to delete the question. It returns True if the user has permission, and False otherwise.
        question = self.get_object()
        return question.author == self.request.user or self.request.user.is_superuser
