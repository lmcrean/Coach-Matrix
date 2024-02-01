# main_forum/views.py

from django.db import models
from django.db.models import Count, F
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Question, STATUS, TeachingStandardTag, Answer
from .forms import AnswerForm, QuestionForm
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
        # Then save the form and instance
        return super(QuestionCreate, self).form_valid(form)
    
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
        standard = question.standard
        print("Standard is:", standard)  # Debug statement
        total_votes = question.number_of_upvotes() - question.number_of_downvotes()

        # Retrieve the sort parameter from the request
        sort_by = request.GET.get('sort_by', 'most_votes')
        print(f"Sort by: {sort_by}")  # Debug print

        # Sort the answers based on the sort_by parameter
        if sort_by == 'most_votes':
            answers = question.answers.filter(approved=True).annotate(total_votes=Count('upvotes') - Count('downvotes')).order_by('-total_votes', '-created_on')
        elif sort_by == 'newest':
            answers = question.answers.filter(approved=True).order_by('-created_on')
        elif sort_by == 'oldest':
            answers = question.answers.filter(approved=True).order_by('created_on')

        for answer in answers:
            print(f"Answer ID: {answer.id}, Total Votes: {getattr(answer, 'total_votes', 'N/A')}, Created On: {answer.created_on}")

        if question.upvotes.filter(id=self.request.user.id).exists(): # If the user has already upvoted the question, set upvoted to True
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
                "standard": standard,
                "total_votes": total_votes,
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

    def post(self, request, slug, *args, **kwargs):
        """
        This function will handle the submission of an answer to a question.
        """
        queryset = Question.objects.filter(status=1)
        question = get_object_or_404(queryset, slug=slug)
        form = AnswerForm(data=request.POST)
        
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.name = request.user.username 
            answer.email = request.user.email
            answer.approved = True
            answer.save()
            
            # Redirect to the question detail page
            return HttpResponseRedirect(reverse('question_detail', args=[slug]))
        else:
            answers = question.answers.filter(approved=True).order_by("-created_on")
            return render(request, 'question_detail.html', {
                'question': question,
                'answers': answers,
                'answer_form': form,  
            })

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

class AnswerUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Answer
    fields = ['body']
    template_name = 'answer_form.html'  # You need to create this template

    def get_success_url(self):
        return reverse_lazy('question_detail', kwargs={'slug': self.object.question.slug})

    def test_func(self):
        return self.request.user == self.get_object().author or self.request.user.is_superuser
        

class AnswerDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Answer
    template_name = 'answer_confirm_delete.html'  # You need to create this template

    def get_success_url(self):
        return reverse_lazy('question_detail', kwargs={'slug': self.object.question.slug})

    def test_func(self):
        answer = self.get_object()
        return self.request.user == answer.author # Ensure only the answer author can delete

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

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'my_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class BookmarkedQuestionsList(LoginRequiredMixin, ListView):
    model = Question
    template_name = 'bookmarked_questions.html'
    context_object_name = 'bookmarked_question_list'

    def get_queryset(self):
        return self.request.user.bookmarks.all()