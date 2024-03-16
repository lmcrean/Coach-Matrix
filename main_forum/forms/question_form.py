# main_forum/forms/question_form.py

# This file contains the form for the Question model. The QuestionForm class will be used to create and update questions in the forum.

from django import forms
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from ..models import Question, Answer
from django_quill.forms import QuillFormField
from taggit.forms import TagField
from django.contrib.auth.forms import PasswordChangeForm
import re


class QuestionForm(forms.ModelForm):
    """
    Form for asking a question as seen in ask_question.html. 
    
    The user can enter a subject line and the main body of the question. They can also tag the question with up to 5 tags. If the user is updating a question, the form needs to be pre-populated with the existing data.
    """
    subject = forms.CharField(
        max_length=200,
        required=True,
        label='Enter your question heading here',
        help_text='Enter a subject line for your question.',
        validators=[MinLengthValidator(10)]
    )
    content = QuillFormField()
    tags = forms.CharField(required=False)


    class Meta:
        """
        the Meta class is used to specify the model to which the form is associated and the fields from the model to include.
        """
        model = Question
        fields = ['subject', 'content', 'tags']

    def __init__(self, *args, **kwargs):
        """
        This is for checking if the form is bound to an existing instance, i.e. if the form is being used to update an existing question.

        self.fields['tags'].widget.attrs['id'] = 'id_tags' is used to add an id to the tags field so that it can be targeted by JavaScript. (yet to be implemented in the project)

        If the form is bound to an existing instance, pre-populate the tags field with the existing tags.
        """
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['tags'].widget.attrs['id'] = 'id_tags'  

        if self.instance.pk: 
            self.fields['tags'].initial = ' '.join(tag.name for tag in self.instance.tags.all()) # Pre-populate the tags field with the existing tags

    def clean_subject(self):
        """
        This method is used to validate the subject field in further detail from the initial class.
        """
        subject = self.cleaned_data.get('subject') # Get the subject from the cleaned data
        subject = re.sub(' +', ' ', subject)  # Replace any multiple spaces with a single space
        if re.search(r"[!£$%^&*()\"\">]", subject):
            raise forms.ValidationError('Special characters are not allowed except "?".')
        # Ensure the subject does not exist already:
        query = Question.objects.filter(subject=subject)
        if self.instance.pk: # If this is an update, exclude the current question from the query
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise forms.ValidationError('A question with this subject already exists.')
        return subject
  

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        return tags

    def save(self, *args, **kwargs):
        instance = super(QuestionForm, self).save(commit=False)
        # Save the instance to ensure it has an ID for many-to-many relationships
        instance.save()

        # Handling tags here
        tags = self.cleaned_data.get('tags', '')
        tag_names = tags.split()  # Split the string into a list of tag names

        # Clear existing tags first if needed, which is important when updating a question
        instance.tags.clear()

        # Add each tag individually
        for tag_name in tag_names:
            instance.tags.add(tag_name.strip())  # Ensure tag is stripped of extra whitespace

        if self.instance.pk:
            # If this is an update, save the instance again
            instance.save()  # Save the instance again to save the many-to-many relationships

        return instance