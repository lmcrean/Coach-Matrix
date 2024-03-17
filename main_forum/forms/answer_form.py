# main_forum/forms/answer_form.py

# This file will contain the form for the Answer model. The AnswerForm class will be used to create and update answers to questions.

from better_profanity import profanity
from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from ..models import Question, Answer
from django_quill.forms import QuillFormField
from taggit.forms import TagField
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
import json
import re
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

def normalize_html(html_content):
    """
    Normalize HTML content by removing HTML tags and normalizing whitespace.
    """
    text_content = strip_tags(html_content)
    normalized_content = ' '.join(text_content.split())
    return normalized_content

class AnswerForm(forms.ModelForm):
    """
    Form for answering a question as seen in question_detail.html. The user can enter the main body of the answer with django_quill module. If the user is updating an answer, the form needs to be pre-populated with the existing data.
    """
    body = QuillFormField(
        validators=[
            MinLengthValidator(50),
            MaxLengthValidator(5000)
        ],
        help_text='Enter the main body of your answer. 50 to 5000 characters.'
    )
    class Meta: 
        """
        Meta class is used to specify the model to which the form is associated
        """
        model = Answer
        fields = ['body']

    def __init__(self, *args, **kwargs):
        """
        This is for checking if the form is bound to an existing instance, i.e. if the form is being used to update an existing answer.

        1. get the request from the kwargs
        2. call the parent __init__ method
        """
        self.request = kwargs.pop('request', None)
        super(AnswerForm, self).__init__(*args, **kwargs)

    def clean(self):
        print("Clean method called") # prints as expected, this is the last line from this view that prints as expected
        super().clean()

    def clean_body(self):
        """
        This method is used to validate the body field in further detail from the initial class.

        1. get the body data from the cleaned data
        2. parse the JSON string to extract the HTML content
        3. check if the HTML content contains any extra new lines or spaces
        4. check if the HTML content contains any profanity
        5. check if the HTML content is between 50 and 5000 characters
        6. check if the HTML content already exists in the database
        """
        body_data = self.cleaned_data.get('body')

        # Attempt to parse the JSON string to extract the HTML content
        try:
            body_json = json.loads(body_data)
            html_content = body_json.get('html', '')
        except json.JSONDecodeError:
            # Handle the error if the body_data is not a valid JSON string
            messages.error(self.request, "Invalid input format. Please ensure your input is correctly formatted.")
            raise ValidationError("Invalid input format. Please ensure your input is correctly formatted.")

        if re.search(r'<br>.*<br>.*<br>', html_content):
            messages.error(self.request, "Please remove any extra new lines from the content of your answer.")
            raise ValidationError("Please remove any extra new lines from the content of your answer.")
        if re.search(r' {3,}', html_content):
            messages.error(self.request, "Please remove any extra spaces from the content of your answer.")
            raise ValidationError("Please remove any extra spaces from the content of your answer.")

        if re.search(r' {3,}', html_content):
            messages.error(self.request, "Please remove any extra spaces from the content of your answer.")
            raise ValidationError("Please remove any extra spaces from the content of your answer.")
        
        if profanity.contains_profanity(html_content):
            messages.error(self.request, "Please remove any profanity from the content of your answer.")
            raise ValidationError("Please remove any profanity from the content of your answer.")

        if len(html_content) < 50:
            messages.error(self.request, "Your answer must be at least 50 characters long.")
            raise ValidationError("Your answer must be at least 50 characters long.")
        if len(html_content) > 5000:
            messages.error(self.request, "Your answer must be no more than 5000 characters long.")
            raise ValidationError("Your answer must be no more than 5000 characters long.")

        normalized_html_content = normalize_html(html_content)
        query = Answer.objects.filter(body__icontains=normalized_html_content)
        if self.instance.pk: # If the instance is being updated
            query = query.exclude(pk=self.instance.pk) # Exclude the current answer if it is being updated
        if query.exists():
            messages.error(self.request, "This answer already exists. Do not copy and paste duplicate answers.")
            raise ValidationError("This answer already exists.")

        return body_data
