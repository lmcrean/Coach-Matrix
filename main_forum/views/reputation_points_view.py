# main_forum/models/reputation_points_view

from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import ReputationPoints


class ReputationView(View):
    """
    This is the view for updating a user's reputation points.
    This view is called when a user upvotes or downvotes a question or answer.
    The view is called from main_forum/views/voting_view.py.

    This is possibly not needed at all, as this could be called in the question
    or answer view, and the user's reputation points could be displayed
    according to the instance.
    """

    def get(self, request, *args, **kwargs):
        """
        This is for getting the user's reputation points and displaying in the
        relevant templates. It is called when:

        1. a user's profile is displayed (yet to implement)
        2. a user is reading the question or answer from a particular question
        instance (yet to implement)

        #2 is probably not needed at all, as this could be called in the
        question or answer view, and the user's reputation points could be
        displayed according to the instance.
        """
        pass

    def post(self, request, *args, **kwargs):
        """
        This is for updating the user's reputation points, after their question
        or answer has been voted. It is called when a user upvotes or downvotes
        a question or answer. The user's reputation points are updated in the
        post method.
        """
        user = request.user
        reputation, created = ReputationPoints.objects.get_or_create(user=user)

        net_votes = reputation.calculate_net_votes()
        reputation.update_reputation_based_on_action('add', 'upvotes')
        reputation.save()

        # return redirect('user_profile', username=user.username)
        pass

    pass
