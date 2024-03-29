# main_forum/views/voting_view.py

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from ..models import Question, Answer, UserProfile, ReputationPoints
import re


class BaseVotingView(LoginRequiredMixin, View):
    """
    Base view for upvoting and downvoting questions and answers. This view is
    inherited by the specific views for each type of vote from QuestionUpvote,
    QuestionDownvote, AnswerUpvote, and AnswerDownvote.

        def post(self, request, *args, **kwargs) is the Method for handling the
        POST request, and is called when a user clicks the upvote or downvote
        button on a question or answer.
            1. If the user has already voted in the opposite direction, a
            message is displayed to remove the existing vote before voting in
            the opposite direction.  opposite_vote_type is used to determine
            the opposite vote type for the object.
            2. If the user has already voted in the same direction, the vote
            is removed.
            3. If the user has not voted, the vote is added. The method then
            calls the get_redirect_url method to redirect the user to the
            appropriate page.

        def get_redirect_url(self, obj) is the Method for getting the redirect
        URL based on the type of object. This method is overridden in the
        specific views for each type of vote to redirect the user to the
        appropriate page after voting.

        def get(self, request, *args, **kwargs) is the Method for handling
        GET requests. This method returns an HttpResponseNotAllowed response
        to prevent users from voting by directly accessing the URL.
    """
    model = None
    vote_type = None

    def post(self, request, *args, **kwargs):
        """
        This method is called when a user clicks the upvote or downvote button
        on a question or answer.

        vote_attr can be upvotes or downvotes

        origin_page is important for determining where on the website the user
        is voting from, e.g. question_list or question_detail

        1. if the user is the author of the question or answer, a message is
        displayed to inform the user that they cannot vote on their own post.
        obj.author is used to determine the author of the object.
        2. If the user has already voted in the opposite direction, a message
        is displayed to remove the existing vote before voting in the opposite
        direction.  opposite_vote_type is used to determine the opposite vote
        type for the object.
        3. If the user has already voted in the same direction, the vote is
        removed instead of added. This is important to prevent users from
        voting multiple times in the same direction.
        4. If the user has not voted, the vote is added.

        The method then calls the get_redirect_url method to redirect the user
        to the appropriate page.
        """
        identifier = kwargs.get('pk') or kwargs.get('slug')
        obj = (
            get_object_or_404(self.model, slug=identifier)
            if 'slug' in kwargs
            else get_object_or_404(self.model, pk=identifier)
        )
        user_profile = UserProfile.objects.get(user=obj.author)
        vote_attr = getattr(obj, self.vote_type)
        opposite_vote_attr = getattr(
            obj, 'downvotes' if self.vote_type == 'upvotes' else 'upvotes')
        vote_already_exists = vote_attr.filter(id=request.user.id).exists()
        action = 'remove' if vote_already_exists else 'add'
        origin_page = request.META.get('HTTP_REFERER', '/')

        if obj.author == request.user:
            messages.error(request, "You cannot vote on your own post.")
            return self.get_redirect_url(obj, origin_page)

        if opposite_vote_attr.filter(id=request.user.id).exists():
            messages.error(
                request,
                "Please remove your existing vote "
                "before voting in the opposite direction."
            )
            return self.get_redirect_url(obj, origin_page)

        if vote_already_exists:
            vote_attr.remove(request.user)
            messages.success(request, "Your vote has been removed.")
        else:
            vote_attr.add(request.user)  # add the vote if it does not exist
            messages.success(request, "Your vote has been added.")

        return self.get_redirect_url(obj, origin_page)

    def get_redirect_url(self, obj, origin_page):
        """
        This method is overridden in the specific views for each type of vote
        to redirect the user to the appropriate page after voting.

        if the object is a question, the method checks the referring page to
        determine the appropriate redirect URL:

            1. If the referring page is the filtered questions page, the method
            redirects the user to the filtered questions page with the same tag
            1.1. If the referring page is the filtered questions page, and the
            user has toggled on most recent votes, the method redirects the
            user to the filtered questions page with the same tag and most
            recent votes.
            1.2 If the referring page is the filtered questions page, and the
            user has toggled on most votes, same as above, but for most votes.

            2. If the referring page is the question list page, the method
            redirects the user to the question list page.
            2.1 If the referring page is the question list page, and the user
            has toggled on most recent votes, the method redirects the user to
            the question list page with most recent votes.
            2.2 If the referring page is the question list page, and the user
            has toggled on most votes, same as above, but for most votes.

            3. If the referring page is the question detail page, the method
            redirects the user to the question detail page for the question
            that was voted on.

        if the object is an answer, the method redirects the user to the
        question detail page for the question that the answer belongs to.
        """
        filtered_questions_pattern = r'/questions/tag/(?P<slug>[\w-]+)/$'
        filtered_questions_pattern_most_recent = (
            r'/questions/tag/(?P<slug>[\w-]+)/\?sort_by=recent')
        filtered_questions_pattern_most_votes = (
            r'/questions/tag/(?P<slug>[\w-]+)/\?sort_by=votes')

        question_list_pattern = r'/questions/$'
        question_list_pattern_most_recent = r'/questions/\?sort_by=recent'
        question_list_pattern_most_votes = r'/questions/\?sort_by=votes'

        question_detail_pattern = r'/(?P<slug>[\w-]+)/$'

        if isinstance(obj, Question):
            """Check for specific filtered questions patterns"""
            if re.search(filtered_questions_pattern_most_recent, origin_page):
                tag_slug = (
                    re.search(
                        filtered_questions_pattern_most_recent, origin_page)
                    .group('slug')
                    )
                return HttpResponseRedirect(
                    reverse(
                        'filter_by_tag',
                        kwargs={'tag_slug': tag_slug}
                    ) + '?sort_by=recent'
                )
            elif re.search(filtered_questions_pattern_most_votes, origin_page):
                tag_slug = re.search(
                    filtered_questions_pattern_most_votes,
                    origin_page).group('slug')
                return HttpResponseRedirect(
                    reverse('filter_by_tag', kwargs={'tag_slug': tag_slug}) +
                    '?sort_by=votes'
                    )
            elif re.search(question_list_pattern_most_recent, origin_page):
                return HttpResponseRedirect(
                    reverse('questions') + '?sort_by=recent'
                )
            elif re.search(question_list_pattern_most_votes, origin_page):
                return HttpResponseRedirect(
                    reverse('questions') + '?sort_by=votes'
                )

            elif re.search(filtered_questions_pattern, origin_page):
                return redirect(
                    'filter_by_tag', tag_slug=re.search(
                        filtered_questions_pattern, origin_page).group('slug')
                )
            elif re.search(question_list_pattern, origin_page):
                return redirect('questions')
            elif re.search(question_detail_pattern, origin_page):
                return redirect('question_detail', slug=obj.slug)
            else:
                # default to questions page in any rare cases,
                # not expecting to use this line
                return redirect('questions')
        elif isinstance(obj, Answer):
            return redirect('question_detail', slug=obj.question.slug)

    def get(self, request, *args, **kwargs):
        """
        only allow POST requests.
        This is to prevent users from voting by directly accessing the URL
        """
        return HttpResponseNotAllowed(['POST'])


class QuestionUpvote(BaseVotingView):
    """ view for upvoting questions using the BaseVotingView class"""
    model = Question
    vote_type = 'upvotes'


class QuestionDownvote(BaseVotingView):
    """ view for downvoting questions using the BaseVotingView class"""
    model = Question
    vote_type = 'downvotes'


class AnswerUpvote(BaseVotingView):
    """ view for upvoting answers using the BaseVotingView class"""
    model = Answer
    vote_type = 'upvotes'

    def get_redirect_url(self, obj, origin_page=None):
        return redirect('question_detail', slug=obj.question.slug)


class AnswerDownvote(BaseVotingView):
    """ view for downvoting answers using the BaseVotingView class """
    model = Answer
    vote_type = 'downvotes'

    def get_redirect_url(self, obj, origin_page=None):
        return redirect('question_detail', slug=obj.question.slug)
