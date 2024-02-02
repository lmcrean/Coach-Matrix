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


class QuestionDetail(View): 
    """
    this class will show the details of a question and it's answers. This was originally from the I Think Therefore I blog walkthrough, and later adapted.
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