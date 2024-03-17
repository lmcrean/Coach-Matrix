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
from django.core.validators import MinLengthValidator, MaxLengthValidator
import re

class AnswerForm(forms.ModelForm) :
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

    def clean_body(self):
        """
        This method is used to validate the body field in further detail from the initial class.

        1. get the body from the cleaned data
        2. check for extra spaces and new lines
        4. check if the body has already been used, using self.instance.pk to exclude the current instance if it exists and the user is updating the answer
        5. check if the body contains any profanity
        6. check if the body is between 50 and 5000 characters
        """
        print("Entering clean_body method")
        body = self.cleaned_data.get('body')
        
        if re.search(r'\n{3,}', body):
            print("Extra new lines found") # this doesn't print
            raise forms.ValidationError("Please remove any extra new lines from the content of your answer.") # this doesn't appear to be working, the user appears to be able to submit the form with extra new lines
        if re.search(r' {3,}', body):
            raise forms.ValidationError("Please remove any extra spaces from the content of your answer.") # working as expected
        if re.search(r"^\s+", body):
            raise forms.ValidationError("Please remove any extra spaces from the beginning of the content of your answer.")
        if re.search(r"\s+$", body):
            raise forms.ValidationError("Please remove any extra spaces from the end of the content of your answer.")
        
        # Check for extra spaces and new lines
        if re.search(r'\n{3,}', body):
            raise forms.ValidationError("Please remove any extra new lines from the content of your answer.") # this doesn't appear to be working, the user appears to be able to submit the form with extra new lines
        if re.search(r' {3,}', body):
            raise forms.ValidationError("Please remove any extra spaces from the content of your answer.")
        if re.search(r"^\s+", body):
            raise forms.ValidationError("Please remove any extra spaces from the beginning of the content of your answer.")
        if re.search(r"\s+$", body):
            raise forms.ValidationError("Please remove any extra spaces from the end of the content of your answer.")
        
        query = Answer.objects.filter(body=body)
        if self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise forms.ValidationError("This content has already been used. You may have already posted this answerm, or it may be copy and pasted. Please enter a new answer.")
        if profanity.contains_profanity(body):
            raise forms.ValidationError("Please remove any profanity from the content of your answer.")
        if len(body) < 50:
            raise forms.ValidationError("Your answer must be at least 50 characters long.") # this doesn't appear to be working, the user appears to be able to submit the form with less than 50 characters
        if len(body) > 5000:
            raise forms.ValidationError("Your answer must be no more than 5000 characters long.") # this doesn't appear to be working, the user appears to be able to submit the form with more than 5000 characters
        return body
