from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils.text import slugify


STATUS = ((0, "Draft"), (1, "Published"))


class TeachingStandardTag(models.Model):
    """
    Model representing the 8 Teaching Standards. This is fed into the Question model as a ManyToManyField.

    The 8 UK Teaching Standards are:
    1. High Expectations
    2. Promoting Progress
    3. Subject Knowledge
    4. Planning
    5. Differentiation
    6. Assessment
    7. Behaviour Management
    8. Professionalism

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
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    upvotes = models.ManyToManyField(
        User, related_name='questionpost_upvotes', blank=True)
    downvotes = models.ManyToManyField(User, related_name='questionpost_downvote', blank=True)
    subject = models.CharField(max_length=100, help_text='Enter a subject line for your question.', unique=True)
    body = models.TextField(null=True, blank=True, default="")  # Allow null and blank, or remove the field if it's not needed
    standards = models.ManyToManyField(TeachingStandardTag, related_name='questions', blank=True)
    answercount = models.IntegerField(default=0)
    views = models.IntegerField(default=0) # number of views

    class Meta: 
        """Meta class is used to change the behavior of the model. By default django orders the objects by their primary key. But we can change this behavior by specifying the ordering attribute in the Meta class.

        In default view for the user, the Questions will be ordered by most upvotes first, then by the date they were created.
        
        in this case, we want several options to be available to us when we query the database for questions. We want to be able to 
        - order the questions by the number of upvotes they have received.
        - order the questions by the date they were created.
        - filter the questions by their Teaching Standards tags.
        """
        ordering = ["-created_on"]
        # ordering = ["-upvotes"]


    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        if not self.pk:  # If this is a new question (no primary key yet)
            self.slug = slugify(self.subject)
            self.title = self.subject  # Set the title based on the subject
        super(Question, self).save(*args, **kwargs)  # Call the "real" save method.

    def number_of_upvotes(self):
        return self.upvotes.count()
    
    def number_of_downvotes(self):
        return self.downvotes.count()

    def save(self, *args, **kwargs):
        # Only set the title and slug if it's a new question or title is not set
        if not self.pk or not self.title:
            self.slug = slugify(self.subject)
            self.title = self.subject
            super(Question, self).save(*args, **kwargs)
        else:
            # If it's an update, the instance already has a primary key
            self.title = self.subject  # The title is updated
            self.slug = slugify(self.subject)  # The slug is updated
            super(Question, self).save(*args, **kwargs)  # The instance is saved again



class Answer(models.Model):
    """
    The Answer model will store the answers to the questions. Users can upvote or downvote answers. The answers will be ordered by the most upvoted answers first, then by the date they were created.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                             related_name="answers")
    slug = models.SlugField(max_length=200, unique=True)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    upvotes = models.ManyToManyField(
        User, related_name='answer_upvote', blank=True)
    downvotes = models.ManyToManyField(User, related_name='answer_downvote', blank=True)
    status = models.IntegerField(choices=STATUS, default=0)
    answercount = models.IntegerField(default=0)
    featured_image = CloudinaryField('image', default='placeholder')

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Answer {self.body} by {self.name}"

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