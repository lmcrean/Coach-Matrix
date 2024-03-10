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

    This should retrieve and attribute the user's reputation points from the main_forum/models/reputation_points_model.py.

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")


    def get_reputation(self):
        """
        This method retrieves the user's reputation points from the main_forum/models/reputation_points_model.py. It's useful for getting the user's reputation points in the template, and centralising the data.
        """
        reputation_points_instance, created = ReputationPoints.objects.get_or_create(user=self.user)
        return reputation_points_instance.reputation

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs): # Ensure reputation is never less than 0
        if self.reputation < 0:
            self.reputation = 0
        super(UserProfile, self).save(*args, **kwargs)

# Signal to create or update user profile upon saving a User instance
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()