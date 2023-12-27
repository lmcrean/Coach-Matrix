# blog/views.py

from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Question, STATUS, TeachingStandardTag, Answer
from .forms import AnswerForm, QuestionForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from django.contrib import messages

class QuestionList(generic.ListView):
    """
    This class will list all the posts using the question model.
    """
    model = Question
    queryset = Question.objects.filter(status=1).order_by("-created_on")
    template_name = "questions.html"
    paginate_by = 6

class QuestionCreate(generic.CreateView): # this class will create a question
    """
    Form for asking a question. The user can enter a subject line and the main body of the question. They can also tag the question with up to 3 standards.

    This class should help create an instance of the Question model. It will also use the QuestionForm class to create the form.

    *args and *kwargs are used to pass a variable number of arguments to a function.
    """
    model = Question
    form_class = QuestionForm  # Use the custom form class
    template_name = "ask_question.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.title = form.cleaned_data['subject']  # Copy the subject into title
        form.instance.slug = form.cleaned_data['subject'].replace(' ', '-').lower()
        # Sets the status to "Published"
        form.instance.status = 1  # '1' corresponds to STATUS = Published. ((0, "Draft"), (1, "Published"))
        return super().form_valid(form)

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

class QuestionDetail(View): 
    """
    this class will show the details of a question. This was originally from the I Think Therefore I blog walkthrough, and later adapted.
    """

    def get(self, request, slug, *args, **kwargs):
        """
        This function will get the details of a post. It will also get the answers associated with the post, and the number of upvotes the post has received.
        """
        queryset = Question.objects.filter(status=1) # Queryset is from the Question model. It filters the questions by status = 1 (published).
        question = get_object_or_404(queryset, slug=slug) # get_object_or_404() retrieves the object that matches the given condition, or an HTTP 404 error if no object matches.
        answers = question.answers.filter(approved=True).order_by("-created_on")
        upvoted = question.upvotes.filter(id=request.user.id).exists()
        downvoted = question.downvotes.filter(id=request.user.id).exists()
        standards = question.standards.all()  # Retrieve associated teaching standard tags
        if question.upvotes.filter(id=self.request.user.id).exists():
            upvoted = True

        return render(
            request,
            "question_detail.html",
            {
                "question": question,
                "answers": answers,
                "answered": False,
                "upvoted": upvoted,
                "downvoted": downvoted,
                "standards": standards,
                "answer_form": AnswerForm()
            },
        )
    
    def question(self, request, slug, *args, **kwargs):
        """
        This function will get the details of a post. It will also get the answers associated with the post, and the number of upvotes the post has received.
        """
        queryset = Question.objects.filter(status=1)
        question = get_object_or_404(queryset, slug=slug)
        answers = question.answers.filter(approved=True).order_by("-created_on")
        upvoted = False
        downvoted = question.downvotes.filter(id=self.request.user.id).exists()

        if question.upvotes.filter(id=self.request.user.id).exists():
            upvoted = True

        answer_form = AnswerForm(data=request.POST)
        if answer_form.is_valid():
            answer_form.instance.email = request.user.email
            answer_form.instance.name = request.user.username
            answer = answer_form.save(commit=False)
            answer.question = question
            answer.save()
        else:
            answer_form = AnswerForm()

        return render(
            request,
            "question_detail.html",
            {
                "question": question,
                "answers": answers,
                "answered": True,
                "answer_form": answer_form,
                "upvoted": upvoted,
                "downvoted": downvoted
            },
        )


class Upvote(View):
    """
    This class will handle upvoting a question. If the user has already upvoted the question, it will remove the upvote. If the user has not already upvoted the question, it will add the upvote.
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
    This class will handle downvoting a question. If the user has already downvoted the question, it will remove the downvote. If the user has not already downvoted the question, it will add the downvote.
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