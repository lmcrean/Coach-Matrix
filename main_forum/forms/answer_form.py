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
        2. remove any extra spaces
        3. remove any extra new lines
        4. check if the body has already been used, using self.instance.pk to exclude the current instance if it exists and the user is updating the answer
        5. check if the body contains any profanity
        """
        body = self.cleaned_data.get('body')
        body = re.sub(' +', ' ', body)
        body = re.sub(r'(\n{3,})', '\n\n', body)
        query = Answer.objects.filter(body=body)
        if self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise forms.ValidationError("This content has already been used.")
        if profanity.contains_profanity(body):
            raise forms.ValidationError("Please remove any profanity from the content.")
        return body