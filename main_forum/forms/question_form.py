# main_forum/forms/question_form.py

# This file contains the form for the Question model.
# The QuestionForm class will be used to create and update questions in the forum.

from better_profanity import profanity
from django import forms
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator
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
    
    The user can enter a subject line and the main body of the question.
    They can also tag the question with up to 5 tags.
    If the user is updating a question, the form needs to be pre-populated
    with the existing data.
    """
    subject = forms.CharField(
        max_length=200,
        required=True,
        label='Enter your question heading here',
        validators=[MinLengthValidator(10)]
    )
    content = QuillFormField(
        validators=[MinLengthValidator(100), MaxLengthValidator(1000)],
        label='Enter the main body of your question.',
        required=True
    )
    tags = forms.CharField(
        required=True,
        label='Enter up to 5 tags separated by spaces'
        )


    class Meta:
        """
        the Meta class is used to specify the model to which the form
        is associated and the fields from the model to include.
        """
        model = Question
        fields = ['subject', 'content', 'tags']

    def __init__(self, *args, **kwargs):
        """
        This is for checking if the form is bound to an existing instance,
        i.e. if the form is being used to update an existing question.

        self.fields['tags'].widget.attrs['id'] = 'id_tags' is used to add an
        id to the tags field so that it can be targeted by JavaScript.
        (yet to be implemented in the project)

        If the form is bound to an existing instance, pre-populate the tags field with the existing tags.
        """
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['tags'].widget.attrs['id'] = 'id_tags'  

        if self.instance.pk: 
            self.fields['tags'].initial = ' '.join(
                tag.name for tag in self.instance.tags.all()
                )
                # Pre-populate the tags field with the existing tags

    def clean_subject(self):
        """
        This method is used to validate the subject field in further detail
        from the initial class.

        1. replace any multiple spaces with a single space
        2. Do not allow special characters except "?". Only allow letters,numbers, commas, full stops, and question marks.
        3. Ensure the subject does not exist already (self.instance.pk is used
        to exclude the current question from the query if this is an update)
        """
        subject = self.cleaned_data.get('subject')
        if re.search(r"^\s+", subject):
            raise forms.ValidationError('The subject cannot start with whitespace.')
        if re.search(r"\s+$", subject):
            raise forms.ValidationError('The subject cannot end with whitespace.')
        if re.search(r"\n", subject):
            raise forms.ValidationError('The subject cannot contain new lines.')
        if re.search(r"\s{2,}", subject):
            raise forms.ValidationError('The subject cannot contain multiple spaces.')
        if re.search(r"[^a-zA-Z0-9,.\s?\'\"-]", subject):
            raise forms.ValidationError('The special character you have used in the subject line is not allowed')
        query = Question.objects.filter(subject=subject)
        if self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise forms.ValidationError('A question with this subject line already exists.')
        if profanity.contains_profanity(subject):
            raise forms.ValidationError('Please remove any profanity from the subject line.')
        return subject
  
    def clean_content(self):
        """
        Clean the content field in further detail from the initial class.

        1. replace any multiple spaces with a single space
        2. replace any multiple new lines with a single new line
        3. Ensure the content does not exist already (exclude the current question if this is an update)
        """
        content = self.cleaned_data.get('content')
        query = Question.objects.filter(content=content)
        if re.search(r"^\s+", content):
            raise forms.ValidationError('The content cannot start with whitespace.')
        if re.search(r"\s+$", content): 
            raise forms.ValidationError('The content cannot end with whitespace.')
        if re.search(r"\s{2,}", content):
            raise forms.ValidationError('The content cannot contain multiple spaces.')
        if re.search(r"\n{3,}", content):
            raise forms.ValidationError('The content cannot contain multiple new lines.')
        if self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise forms.ValidationError('This content has already been used. Do not copy and paste the same content.')
        if profanity.contains_profanity(content):
            raise forms.ValidationError('Please remove any profanity from the content.')
        return content

    def clean_tags(self):
        """
        Clean the tags field to ensure:
        1. There are between 1 and 5 tags.
        2. Each tag is between 3 and 20 characters in length.
        3. Multiple spaces within tags are collapsed to a single space.
        4. Return keys are not considered.
        """
        tags_string = self.cleaned_data.get('tags', '')

        # remove any extra spaces from the tags
        tags_string = re.sub(' +', ' ', tags_string)

        # split the tags string into a list of tag names
        tags_list = tags_string.split()

        if tags_string.startswith(' '):
            raise forms.ValidationError('Tags cannot start with whitespace.')
        if tags_string.endswith(' '):
            raise forms.ValidationError('Tags cannot end with whitespace.')
        if re.search(r"\n", tags_string):
            raise forms.ValidationError('Tags cannot contain new lines.')
        if re.search(r"\s{2,}", tags_string):
            raise forms.ValidationError('Tags cannot contain multiple spaces.')
        if profanity.contains_profanity(tags_string):
            raise forms.ValidationError('Please remove any profanity from the tags.')
        if not 1 <= len(tags_list) <= 5:
            raise forms.ValidationError(
                'Please provide between 1 and 5 tags.'
                )
        for tag in tags_list:
            if not 3 <= len(tag) <= 20:
                raise forms.ValidationError(
                    'Each tag must be between 3 and 20 characters.'
                    )
        
        return ' '.join(tags_list)

    def save(self, *args, **kwargs):
        """
        Save the instance and handle the tags.
        This method is used to save the instance.
        The tags are handled separately to ensure they are added to the
        instance after it has been saved.

        1. Define the instance to be saved as the form instance.
        2. Save the instance to ensure it has an ID for many-to-many
        relationships.
        3. Get the tags string from the cleaned data.
        4. Split the tags string into a list of tag names.
        5. Clear existing tags if needed, which is important when updating
        a question.
        6. Add each tag individually and ensure it is stripped of extra
        whitespace.
        7. If this is an update (self.instance.pk),
        save the instance again to save the many-to-many relationships.
        """
        instance = super(QuestionForm, self).save(commit=False)
        instance.save()
        tags = self.cleaned_data.get('tags', '')
        tag_names = tags.split()
        instance.tags.clear()
        for tag_name in tag_names:
            instance.tags.add(tag_name.strip())
        if self.instance.pk:
            instance.save()

        return instance