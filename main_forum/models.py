# main_forum/models.py

from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils import timezone
from datetime import timedelta
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django_quill.fields import QuillField
from django.db.models.signals import m2m_changed
from django.dispatch import receiver



STATUS = ((0, "Draft"), (1, "Published"))


class TeachingStandardTag(models.Model):
    """
    Model representing the 8 Teaching Standards. This is fed into the Question model as a ManyToManyField. The tags were added manually on Django Admin.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Question(models.Model):
    """
    This class will create a user question along with the question's title, slug, author, featured image, excerpt, updated_on, content, created_on, status, upvotes, downvotes, subject, body, standards, answercount, and views.

    Key Parameters: The body can be no longer than 10000 characters. When choosing teacher standard, they can tag the question with up to 3 standards.
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True) # slug is a human-readable unique identifier for an object, which is used in URLs. It is usually a hyphenated lowercase version of the title.
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="question_posts"
    )
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = QuillField()
    updated_on = models.DateTimeField(auto_now=True)
    content = QuillField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    upvotes = models.ManyToManyField(
        User, related_name='questionpost_upvotes', blank=True)
    downvotes = models.ManyToManyField(User, related_name='questionpost_downvote', blank=True)
    subject = models.CharField(max_length=100, help_text='Enter a subject line for your question.', unique=True)
    body = RichTextField(null=True, blank=True, default="")  # Allow null and blank, or remove the field if it's not needed
    standard = models.ForeignKey(TeachingStandardTag, related_name='questions', on_delete=models.SET_NULL, null=True, blank=True)
    answercount = models.IntegerField(default=0)
    views = models.IntegerField(default=0) # number of views
    net_votes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Determine whether this is a new instance or an update
        is_new = self._state.adding

        # Handling slug and title creation or update
        if not self.pk:  # If this is a new question
            self.slug = slugify(self.subject)
            self.title = self.subject

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

# Signal handlers to update net_votes when upvotes or downvotes change
@receiver(m2m_changed, sender=Question.upvotes.through)
@receiver(m2m_changed, sender=Question.downvotes.through)
def update_net_votes(sender, instance, **kwargs):
    instance.net_votes = instance.upvotes.count() - instance.downvotes.count()
    instance.save()



class Answer(models.Model):
    """
    The Answer model will store the answers to the questions. Users can upvote or downvote answers. The answers will be ordered by the most upvoted answers first, then by the date they were created.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                             related_name="answers")
    slug = models.SlugField(max_length=200, unique=True)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = QuillField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    upvotes = models.ManyToManyField(
        User, related_name='answer_upvote', blank=True)
    downvotes = models.ManyToManyField(User, related_name='answer_downvote', blank=True)
    status = models.IntegerField(choices=STATUS, default=0)
    answercount = models.IntegerField(default=0)
    featured_image = CloudinaryField('image', default='placeholder')
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Answer {self.body} by {self.name}"

    def number_of_upvotes(self):
        return self.upvotes.count()
    
    def number_of_downvotes(self):
        return self.downvotes.count()
    
    def total_votes(self):
        return self.number_of_upvotes() - self.number_of_downvotes()

    def save(self, *args, **kwargs):
        if not self.slug:  # if slug is not set or empty
            base_slug = slugify(self.name) if self.name else 'answer'  # Fallback to 'answer' if name is empty
            new_slug = base_slug
            counter = 1

            while Answer.objects.filter(slug=new_slug).exists():  # Ensure uniqueness
                new_slug = f'{base_slug}-{counter}'
                counter += 1

            self.slug = new_slug or uuid.uuid4().hex[:6]  # Set a UUID if all else fails

        super(Answer, self).save(*args, **kwargs)
    
    
class Upvote(models.Model):
    """
    This class will handle upvoting a question. If the user has already upvoted the question, it will remove the upvote. If the user has not already upvoted the question, it will add the upvote.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    upvotedate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + " upvoted " + str(self.question) + " on " + str(self.upvotedate)
    
class Downvote(models.Model):
    """
    This class will handle downvoting a question. If the user has already downvoted the question, it will remove the downvote. If the user has not already downvoted the question, it will add the downvote.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    downvotedate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + " downvoted " + str(self.question) + " on " + str(self.downvotedate)