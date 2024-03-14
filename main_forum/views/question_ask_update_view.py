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
        return super().form_valid(form)

    def form_invalid(self, form):
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
        return self.get_object().author == self.request.user or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        """
        This function should get context data. At present it retrieves subject and content correctly, however tags appear as [<Tag: tag1>, <Tag: tag2>, <Tag: tag3>, <Tag: tag4>, <Tag: tag5>] when expected to be tag1 tag2 tag3 tag4 tag5.
        """
        context = super(QuestionUpdateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(instance=self.object)
        context['question'] = self.get_object()
        return context

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
        
        if form.is_valid():
            # Check if the subject has changed and if the new subject already exists
            subject = form.cleaned_data.get('subject')
            if subject != self.object.subject and Question.objects.filter(subject=subject).exclude(pk=self.object.pk).exists():
                form.add_error('subject', 'A question with this subject already exists.')
                return self.form_invalid(form)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    