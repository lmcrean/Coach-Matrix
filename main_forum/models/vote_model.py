# main_forum/models/vote_model.py

# this file will contain the models for the main_forum app.
# The models will include the Question, Answer, Upvote, Downvote, UserProfile,
# and Bookmark classes.

from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils import timezone
from datetime import timedelta
from django.utils.text import slugify
from django_quill.fields import QuillField
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from taggit.managers import TaggableManager
from .question_model import Question
from .user_profile_model import User


class Upvote(models.Model):
    """
    This class will handle upvoting a question.
    If the user has already upvoted the question, it will remove the upvote.
    If the user has not already upvoted the question, it will add the upvote.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    upvotedate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} upvoted {self.question} on {self.upvotedate}"


class Downvote(models.Model):
    """
    This class will handle downvoting a question.
    If the user has already downvoted the question,it will remove the
    downvote.
    If the user has not already downvoted the question, it will add the
    downvote.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    downvotedate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} upvoted {self.question} on {self.downvotedate}"
