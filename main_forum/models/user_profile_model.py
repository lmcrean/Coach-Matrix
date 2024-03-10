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

class UserProfile(models.Model):
    """
    This stores additional information to the Django User model, including the user's reputation points. The reputation points are calculated based on the user's upvotes and downvotes.

    This is particularly important when the question author's reputation points are called, as the author's reputation points are retrieved from the Reputation Points model through {{ question.author.reputation_points.reputation }} in the question model.

    This is currently in testing
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    reputation = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs): # Ensure reputation is never less than 0
        if self.reputation < 0:
            self.reputation = 0
        super(UserProfile, self).save(*args, **kwargs)

# Signal to create or update user profile upon saving a User instance. Need to establish if still needed.
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()
    super().save(*args, **kwargs) # super() is used to call the parent class's method. In this case, it is used to call the save method of the parent class, which is the User model. This is used to ensure that the user profile is saved when the user is saved.