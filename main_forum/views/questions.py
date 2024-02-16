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

class QuestionCreateView(LoginRequiredMixin, generic.CreateView):
    """ view for creating a new question."""
    model = Question
    form_class = QuestionForm
    template_name = "ask_question.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 1
        # Debugging print statement
        print("Form is valid, saving question...")
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.cleaned_data)
        print(form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('questions')

class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    """ view for updating a question. This should only be accessible to the author of the question. """
    model = Question
    form_class = QuestionForm
    template_name = 'ask_question.html'
    context_object_name = 'question' # context_object_name is a variable that is used to specify the name of the variable that will be used to access the object in the template.
    print("QuestionUpdateView")

    def test_func(self): # test_func is a method that is called to check if the user has permission to update the question. It returns True if the user has permission, and False otherwise.
        print("test_func")
        print(self.get_object().author)
        return self.get_object().author == self.request.user or self.request.user.is_superuser

    def form_valid(self, form):
    # Only update the slug if the subject has changed
        if form.instance.subject != self.object.subject:
            form.instance.slug = slugify(form.cleaned_data.get('subject'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('question_detail', kwargs={'slug': self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        print("Post")
        
        if form.is_valid():
            # Check if the subject has changed and if the new subject already exists
            subject = form.cleaned_data.get('subject')
            print("Subject:", subject)
            if subject != self.object.subject and Question.objects.filter(subject=subject).exclude(pk=self.object.pk).exists():
                print("A question with this subject already exists, excluding pk self.")
                form.add_error('subject', 'A question with this subject already exists.')
                return self.form_invalid(form)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super(QuestionUpdateView, self).get_context_data(**kwargs)
        context['question'] = self.get_object()
        print("get Context:", context)
        return context

class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Question
    template_name = "question_delete.html"
    success_url = reverse_lazy('questions')

    def test_func(self): # test_func is a method that is called to check if the user has permission to delete the question. It returns True if the user has permission, and False otherwise.
        question = self.get_object()
        return question.author == self.request.user or self.request.user.is_superuser
