# main_forum/views/question_ask_update_view.py

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from ..models import Question
from ..forms import QuestionForm

class QuestionCreateView(LoginRequiredMixin, generic.CreateView):
    """ view for creating a new question."""
    model = Question
    form_class = QuestionForm
    template_name = "ask_question.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 1
        # Debugging print statement
        print("Form is valid, saving question...") # PASS
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
    template_name = 'update_question.html'
    context_object_name = 'question' # context_object_name is a variable that is used to specify the name of the variable that will be used to access the object in the template.

    def test_func(self): # test_func is a method that is called to check if the user has permission to update the question. It returns True if the user has permission, and False otherwise.
        print("test_func") # PASS
        print(self.get_object().author) # PASS e.g. lmcrean
        return self.get_object().author == self.request.user or self.request.user.is_superuser

    def form_valid(self, form):
    # Only update the slug if the subject has changed
        if form.instance.subject != self.object.subject:
            print("Updating slug") # testing
            form.instance.slug = slugify(form.cleaned_data.get('subject'))
        else:
            print("Slug not updated") # testing
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('question_detail', kwargs={'slug': self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        print("Post") # FAIL, possibly working but not printing
        
        if form.is_valid():
            # Check if the subject has changed and if the new subject already exists
            subject = form.cleaned_data.get('subject')
            print("Subject:", subject) # FAIL, not printing
            if subject != self.object.subject and Question.objects.filter(subject=subject).exclude(pk=self.object.pk).exists():
                print("A question with this subject already exists, excluding pk self.") # FAIL, possibly working but not printing
                form.add_error('subject', 'A question with this subject already exists.')
                return self.form_invalid(form)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super(QuestionUpdateView, self).get_context_data(**kwargs)
        context['question'] = self.get_object()
        print("get Context:", context) # PASS USING TAGS  tag1 tag2 tag3 : prints: get Context: {'object': <Question: test for updating Q>, 'question': <Question: test for updating Q>, 'form': <QuestionForm bound=False, valid=Unknown, fields=(subject;content;tags)>, 'view': <main_forum.views.questions.QuestionUpdateView object at 0x7f20094617c0>} 
        return context