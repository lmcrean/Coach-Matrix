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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    reputation = models.IntegerField(default=0)

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