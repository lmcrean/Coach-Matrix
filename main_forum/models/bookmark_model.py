# main_forum/models/bookmark_model.py

# this file will contain the models for the main_forum app. The models will include the Question, Answer, Upvote, Downvote, UserProfile, and Bookmark classes.

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

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="bookmarked_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f'{self.user.username} bookmarked {self.question.subject}'