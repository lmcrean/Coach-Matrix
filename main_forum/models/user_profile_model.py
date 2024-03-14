# main_forum/user_profile_model.py

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
from .reputation_points_model import ReputationPoints

class UserProfile(models.Model):
    """
    This stores additional information to the Django User model, including the user's reputation points. The reputation points are calculated based on the user's upvotes and downvotes.

    This is particularly important when the question author's reputation points are called, as the author's reputation points are retrieved from the Reputation Points model through {{ question.author.reputation_points.reputation }} in the question model.

    This is currently in testing
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user_profile_and_reputation(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
        ReputationPoints.objects.get_or_create(user=instance)