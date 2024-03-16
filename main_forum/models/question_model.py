# main_forum/models/question_model.py

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

STATUS = ((0, "Draft"), (1, "Published"))

class Question(models.Model):
    """
    This class will create a user question along with the question's subject, slug, author, featured image, excerpt, updated_on, content, created_on, status, upvotes, downvotes, subject, body, standards, answercount, and views.

    Key Parameters: The body can be no longer than 10000 characters. When choosing teacher standard, they can tag the question with up to 3 standards.

    Reputation points are retrieved through {{ question.author.reputation_points.reputation }}
    """
    subject = models.CharField(max_length=200, help_text='Enter a subject line for your question.', unique=True)
    slug = models.SlugField(max_length=200, unique=True) # slug is a human-readable unique identifier for an object, which is used in URLs. It is usually a hyphenated lowercase version of the subject.
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="question_posts"
    )
    updated_on = models.DateTimeField(auto_now=True)
    content = QuillField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    upvotes = models.ManyToManyField(
        User, related_name='questionpost_upvotes', blank=True)
    downvotes = models.ManyToManyField(User, related_name='questionpost_downvote', blank=True)
    answercount = models.IntegerField(default=0)
    views = models.IntegerField(default=0) 
    net_votes = models.IntegerField(default=0)
    tags = TaggableManager()

    @property
    def author_reputation(self):
        """
        This is a property that retrieves the user's reputation points from the user's profile. There should be one author_reputation for each question instance.

        it is called in the question template to display the author's reputation points with {{ question.author_reputation }}.

        If there is an error, it should return 0.

        This is currently in testing.
        """
        return self.author.reputation_points.reputation if hasattr(self.author, 'reputation_points') else 0
    
    def save(self, *args, **kwargs):
        # Determine whether this is a new instance or an update
        is_new = self._state.adding

        # Handling slug and subject creation or update
        if not self.pk:  # If this is a new question
            self.slug = slugify(self.subject)

        # Save the instance first (for both new and updated instances)
        super(Question, self).save(*args, **kwargs)

        # Recalculate net_votes only for an update
        if not is_new:
            self.net_votes = self.upvotes.count() - self.downvotes.count()
            # Save again to update net_votes
            super(Question, self).save(update_fields=['net_votes'])


    class Meta:
        """By default django orders the objects by their primary key. But we can change this behavior by specifying the ordering attribute in the Meta class.
        """
        ordering = ["-created_on"]

    def __str__(self):
        return self.subject

    def number_of_upvotes(self): # method to count the number of upvotes
        return self.upvotes.count()
    
    def number_of_downvotes(self): # method to count the number of downvotes
        return self.downvotes.count()

    def formatted_date(self): # method to format the date responsively to the time it was created
        now = timezone.now()
        if now - timedelta(days=1) < self.created_on: # if the question was created less than a day ago
            return self.created_on.strftime('%-I:%M%p').lower() # display the time as e.g. 9:30am
        elif now - timedelta(days=7) < self.created_on: # elif the question was created less than a week ago
            return self.created_on.strftime('%-I:%M%p, %b %d') # display the time and date as e.g. 9:30am, Jan 6
        elif self.created_on.year == now.year: # elif the question was created this year
            return self.created_on.strftime('%b %d') # display the date as e.g. Jan 6
        else:
            return self.created_on.strftime('%b %d, %Y') # else the question was created in a previous year

@receiver(m2m_changed, sender=Question.upvotes.through)
@receiver(m2m_changed, sender=Question.downvotes.through)
def update_net_votes(sender, instance, **kwargs):
    """
    Update net votes when upvotes or downvotes change.
    
    Need to test if this is still needed.
    """
    instance.net_votes = instance.upvotes.count() - instance.downvotes.count()
    instance.save()
