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
        """
        super(AnswerForm, self).__init__(*args, **kwargs)

    def clean(self):
        print("Clean method called") # prints as expected, this is the last line from this view that prints as expected
        super().clean()

    def clean_body(self):
        """
        This method is used to validate the body field in further detail from the initial class.

        1. get the body from the cleaned data
        2. check for extra spaces and new lines
        4. check if the body has already been used, using self.instance.pk to exclude the current instance if it exists and the user is updating the answer
        5. check if the body contains any profanity
        6. check if the body is between 50 and 5000 characters
        """
        print("Entering clean_body method") # not working working as expected, not printing from here when expected
        body_data = self.cleaned_data.get('body')
        print(f"Body data before cleaning: {body_data}")

        # Attempt to parse the JSON string to extract the HTML content
        try:
            body_json = json.loads(body_data)
            html_content = body_json.get('html', '')
        except json.JSONDecodeError:
            # Handle the error if the body_data is not a valid JSON string
            raise forms.ValidationError("Invalid input format. Please ensure your input is correctly formatted.")

        if re.search(r'<br>.*<br>.*<br>', html_content):
            print("Extra new lines found")
            messages.error("Please remove any extra new lines from the content of your answer.")
            raise forms.ValidationError("Please remove any extra new lines from the content of your answer.")

        if re.search(r' {3,}', html_content):
            raise forms.ValidationError("Please remove any extra spaces from the content of your answer.") # working as expected
        
        if profanity.contains_profanity(html_content):
            raise forms.ValidationError("Please remove any profanity from the content of your answer.")

        if len(html_content) < 50:
            raise forms.ValidationError("Your answer must be at least 50 characters long.")
        if len(html_content) > 5000:
            raise forms.ValidationError("Your answer must be no more than 5000 characters long.")

        return body_data
