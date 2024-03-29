# main_forum/views/question_detail_and_answers_view

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View, UpdateView, DeleteView
from ..models import Question, Answer
from ..forms import AnswerForm
from django.contrib import messages


class QuestionDetail(View):
    """
    View for displaying a question and its answers.

    This view will display the question and its answers, and allow the user to
    post a new answer. The user will also be able to sort the answers by most
    votes, newest, or oldest.
    """
    def get(self, request, slug, *args, **kwargs):
        """
        Get the question and its answers, and render the question detail page.
        """
        question = self.get_question(slug)
        answers, sort_by = self.get_sorted_answers(question)
        upvoted, downvoted, total_votes = (
            self.get_voting_status(question, request.user)
            )

        return render(request, "question_detail.html", {
            "question": question,
            "answers": answers,
            "answered": False,  # Will revise this based on actual logic needed
            "upvoted": upvoted,
            "downvoted": downvoted,
            "total_votes": total_votes,
            "answer_form": AnswerForm(),
            "sort_by": sort_by,
        })

    def post(self, request, slug, *args, **kwargs):
        """
        Post a new answer to the question.
        """
        question = self.get_question(slug)
        form = AnswerForm(data=request.POST, request=request)

        if form.is_valid():
            """
            if the form is valid, save the answer and redirect to the question
            detail page
            """
            self.save_answer(form, question, request.user)
            return redirect('question_detail', slug=slug)
        else:
            answers, _ = self.get_sorted_answers(question)
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"{error}")
            return render(request, 'question_detail.html', {
                'question': question,
                'answers': answers,
                'answer_form': form,
            })

    def get_question(self, slug):
        """
        Get the question with the given slug, or return a 404 response if the
        question does not exist.
        """
        return get_object_or_404(Question.objects.filter(status=1), slug=slug)

    def get_sorted_answers(self, question):
        """
        Get the answers to the question, sorted by the requested sort order.
        sort_by defaults to sorting most votes.

        Annotate() method in if loop calculates the total_votes variable for
        each object, which is the difference between the number of upvotes and
        downvotes.nThen we sort by this field in descending order, and by
        created_on in descending order as a tiebreaker.
        """
        sort_by = self.request.GET.get('sort_by', 'most_votes')
        if sort_by == 'most_votes':
            answers = (
                question.answers.filter(approved=True)
                .annotate(total_votes=Count('upvotes') - Count('downvotes'))
                .order_by('-total_votes', '-created_on')
                )
        elif sort_by == 'newest':
            answers = (
                question.answers.filter(approved=True).order_by('-created_on')
                )
        elif sort_by == 'oldest':
            answers = (
                question.answers.filter(approved=True).order_by('created_on')
                )
        return answers, sort_by

    def get_voting_status(self, question, user):
        """
        Get the voting status for the given question and user.

        1. Check if the user has upvoted the question...
        2. Check if the user has downvoted the question...
        3. ...and calculate the total number of votes based on total upvotes
        and downvotes assigned to the question
        """
        upvoted = question.upvotes.filter(id=user.id).exists()
        downvoted = question.downvotes.filter(id=user.id).exists()
        total_votes = (
            question.number_of_upvotes() - question.number_of_downvotes())
        return upvoted, downvoted, total_votes

    def save_answer(self, form, question, user):
        """
        Save the answer to the question.
        """
        answer = form.save(commit=False)
        answer.author = user
        answer.question = question
        answer.approved = True
        answer.save()


class AnswerUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update an answer using a form"""
    model = Answer
    fields = ['body']
    template_name = 'answer_form.html'

    def get_success_url(self):
        """
        Redirect to the question detail page after updating the answer.

        We use reverse_lazy() here because we are in a class-based view,
        and we need to pass the slug of the question to the URL pattern.
        """
        return (
            reverse_lazy(
                'question_detail',
                kwargs={'slug': self.object.question.slug}
                )
        )

    def test_func(self):
        """Check if the current user is the author of the answer"""
        return (
            self.request.user == self.get_object().author or
            self.request.user.is_superuser
        )


class AnswerDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ Delete an answer """
    model = Answer
    template_name = 'answer_confirm_delete.html'

    def get_success_url(self):
        return (
            reverse_lazy(
                'question_detail',
                kwargs={'slug': self.object.question.slug}
                )
        )

    def test_func(self):
        """
        check if user is author of the answer before deleting.
        We also allow superusers to delete answers.
        """
        answer = self.get_object()
        return (
            self.request.user == answer.author or
            self.request.user.is_superuser
        )
