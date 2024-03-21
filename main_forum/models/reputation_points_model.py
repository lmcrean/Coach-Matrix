# main_forum/models/reputation_points_model.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone
from datetime import timedelta
from django.utils.text import slugify
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver


class ReputationPoints(models.Model):
    """
    AT PRESENT, THIS CLASS IS NOT BEING USED IN THE APPLICATION.
    IT IS A WORK IN PROGRESS.

    This class will create a user's reputation points along with the user,
    reputation, and date awarded.

    Each user has their own reputation points.

    Key Parameters: The reputation can be no longer than 10000 characters.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="reputation_points")
    reputation = models.IntegerField(default=0)
    date_awarded = models.DateTimeField(auto_now_add=True)

    def calculate_net_votes(self):
        """
        This method calculates the user's net votes based on the user's upvotes
        and downvotes on questions and answers. The net votes are used to
        calculate the user's reputation points.

        This function should be called whenever a user's reputation points are
        updated, and the user's reputation points should be updated whenever a
        vote is added or removed.

        This is currently being tested.

        Imports are used here to avoid circular import.
        Circular import occurs when two or more modules depend on each other.
        In this case, the UserProfile model depends on the Question and Answer
        models, and the Question and Answer models depend on the UserProfile
        model.
        """

        from .models import Question, Answer
        question_upvotes = sum(
            question.upvotes.count()
            for question in Question.objects.filter(author=self.user))
        question_downvotes = sum(
            question.downvotes.count()
            for question in Question.objects.filter(author=self.user))
        answer_upvotes = sum(
            answer.upvotes.count()
            for answer in Answer.objects.filter(author=self.user))
        answer_downvotes = sum(
            answer.downvotes.count()
            for answer in Answer.objects.filter(author=self.user))

        net_votes = (
            question_upvotes + answer_upvotes
            - question_downvotes - answer_downvotes
            )

        if net_votes < 0:
            net_votes = 0
        return net_votes

    def update_reputation_based_on_action(self, action, vote_type):
        """
        This method is called when a vote is added or removed in
        main_forum/views/voting_view.py.

        It updates the user's reputation based on the action and vote type.
        Reputation points are capped at 0.
        After each vote, reputation never increments by more than 1 per vote,
        and never decrement by more than 1 per vote.

        VALIDATION CRITERIA for REPUTATION POINTS
            1. Rep points never go below 0, if a user on 0 rep points recieves
            a downvote then the -1 is discounted to remain at 0 instead of -1
            2. If user A recieves 4 negative points from  User B, then has one
            negative vote removed, it should stay at 0. Only positive votes
            can add reputation points, providing the user has more positive
            votes than negative votes.
            3. Rep points can't increase by more than 1 per vote, and can't
            decrease by more than 1 per vote

        This is currently being tested.
        It should update the user's reputation based on the action
        and vote type.
        """
        if action == 'add':
            if vote_type == 'upvotes':
                self.reputation += 1
            elif vote_type == 'downvotes':
                self.reputation -= 1
        elif action == 'remove':
            if vote_type == 'upvotes':
                self.reputation -= 1
            elif vote_type == 'downvotes':
                self.reputation += 1

        # Ensure reputation does not fall below 0
        self.reputation = max(self.reputation, 0)
        self.save()

    def update_reputation_after_user_deletes_profile(self):
        """
        1. if user A has a mix of upvotes frrom User B and downvotes from
        User C, and then user B with upvotes deletes their account, then User
        A's reputation points are capped at 0 instead of a negative value
        2. if user A has 7 reputation points, a mix of 5 upvotes from User B
        and 2 upvotes from User C, and then user B with upvotes deletes their
        account, then User A's reputation points reduces from 7 to 2
        reputation points.

        This is not yet implemented.
        """
        pass

    def update_user_A_reputation_after_delete_own_post(self):
        """
        We can replace the validation criteria with questions instead of
        answers, and the same logic should apply.

        Validation criteria:
            1.
            User A has an answer with 5 upvotes and 2 downvotes,
            with 5 net votes including from other content.
            User A deletes their answer, thereby losing their reputation
            points.
            User A's reputation points are capped at 2 instead of a negative
            value, since they have lost 3 reputation points.

            2.
            User A has an answer with 8 upvotes and 2 downvotes, with 2 net
            votes including from other content. User A deletes their answer,
            thereby losing their reputaiton points. User A's reputation points
            are reduced from 2 to 0, since after falling in to negative points,
            the reputation points are capped at 0.

        This is not yet implemented.
        """
        pass

    def __str__(self):
        return f"{self.user.username} - {self.reputation} points"

    class Meta:
        verbose_name = "Reputation Point"
        verbose_name_plural = "Reputation Points"
