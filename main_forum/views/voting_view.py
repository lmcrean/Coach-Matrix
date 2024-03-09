from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from ..models import Question, Answer, UserProfile
import re

class BaseVotingView(LoginRequiredMixin, View):
    """
    Base view for upvoting and downvoting questions and answers. This view is inherited by the specific views for each type of vote from QuestionUpvote, QuestionDownvote, AnswerUpvote, and AnswerDownvote.

        def post(self, request, *args, **kwargs) is the Method for handling the POST request, and is called when a user clicks the upvote or downvote button on a question or answer. 
            1. If the user has already voted in the opposite direction, a message is displayed to remove the existing vote before voting in the opposite direction.  opposite_vote_type is used to determine the opposite vote type for the object. 
            2. If the user has already voted in the same direction, the vote is removed. 
            3. If the user has not voted, the vote is added. The method then calls the get_redirect_url method to redirect the user to the appropriate page.
        
        def get_redirect_url(self, obj) is the Method for getting the redirect URL based on the type of object. This method is overridden in the specific views for each type of vote to redirect the user to the appropriate page after voting.

        def get(self, request, *args, **kwargs) is the Method for handling GET requests. This method returns an HttpResponseNotAllowed response to prevent users from voting by directly accessing the URL.
    """
    model = None
    vote_type = None

    def update_reputation(self, user_profile, action, vote_type):
        """
        Update the user's reputation based on the action and vote type.
        Actions: 'add' or 'remove'
        Vote types: 'upvotes' or 'downvotes'

        VALIDATION CRITERIA for REPUTATION POINTS
            1. Rep points never go below 0, if a user on 0 rep points recieves a downvote then the -1 is discounted to remain at 0 instead of -1
            2. if user A has a mix of upvotes frrom User B and downvotes from User C, and then user B with upvotes deletes their account, then User A's reputation points are capped at 0 instead of a negative value 
            3. if user A has 7 reputation points, a mix of 5 upvotes frrom User B and 2 upvotes from User C, and then user B with upvotes deletes their account, then User A's reputation points reduces from 7 to 2 reputation points
            4. If user A recieves 4 negative points from  User B, then has one negative vote removed, it should stay at 0. Only positive votes can add reputation points, providing the user has more positive votes than negative votes.
        """
        net_votes = user_profile.user.question_upvotes.count() + user_profile.user.answer_upvotes.count() - user_profile.user.question_downvotes.count() - user_profile.user.answer_downvotes.count()

        if action == 'add':
            if vote_type == 'upvotes':
                user_profile.reputation += 1
            elif vote_type == 'downvotes' and net_votes > 0:
                user_profile.reputation = max(user_profile.reputation - 1, 0)
        elif action == 'remove':
            if vote_type == 'upvotes' and net_votes >= 0:
                user_profile.reputation = max(user_profile.reputation - 1, 0)
            elif vote_type == 'downvotes' and net_votes > 0:
                user_profile.reputation += 1

        user_profile.save()

    def post(self, request, *args, **kwargs):
        identifier = kwargs.get('pk') or kwargs.get('slug')
        obj = get_object_or_404(self.model, slug=identifier) if 'slug' in kwargs else get_object_or_404(self.model, pk=identifier)
        user_profile = UserProfile.objects.get(user=obj.author)

        if obj.author == request.user:
            messages.error(request, "You cannot vote on your own post.")
            return self.get_redirect_url(obj)

        vote_attr = getattr(obj, self.vote_type)
        opposite_vote_attr = getattr(obj, 'downvotes' if self.vote_type == 'upvotes' else 'upvotes')

        if opposite_vote_attr.filter(id=request.user.id).exists():
            messages.error(request, "Please remove your existing vote before voting in the opposite direction.")
            return self.get_redirect_url(obj)

        vote_already_exists = vote_attr.filter(id=request.user.id).exists()

        if vote_already_exists:
            vote_attr.remove(request.user)
            self.update_reputation(user_profile, 'remove', self.vote_type)
            messages.success(request, "Your vote has been removed.")
        else:
            vote_attr.add(request.user)
            self.update_reputation(user_profile, 'add', self.vote_type)
            messages.success(request, "Your vote has been added.")

        return self.get_redirect_url(obj)


    def get_redirect_url(self, obj, origin_page):
        if origin_page:  # Only proceed if origin_page is not an empty string
            match = re.search(tag_regex, origin_page)
            if match:
                # If origin_page matches the filtered tag list pattern, redirect back to that filtered list
                tag_name = match.group(1)
                return HttpResponseRedirect(reverse('filtered_questions', args=[tag_name]))
        elif origin_page == 'questions_list':
            return HttpResponseRedirect(reverse('questions'))
        elif isinstance(obj, Question):
            return HttpResponseRedirect(reverse('question_detail', args=[obj.slug]))
        elif isinstance(obj, Answer):
            return HttpResponseRedirect(reverse('question_detail', kwargs={'slug': obj.question.slug}))
        else:
            return HttpResponseRedirect('/')


    def get(self, request, *args, **kwargs): # only allow POST requests. This is to prevent users from voting by directly accessing the URL
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
