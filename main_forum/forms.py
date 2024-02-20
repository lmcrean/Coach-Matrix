# main_forum/forms.py

# This file will contain the forms for the main_forum app. The forms will include the QuestionForm and AnswerForm classes.

from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Question, Answer
from django_quill.forms import QuillFormField
from taggit.forms import TagField
from django.contrib.auth.forms import PasswordChangeForm



class QuestionForm(forms.ModelForm):
    """
    Form for asking a question as seen in ask_question.html. 
    
    The user can enter a subject line and the main body of the question. They can also tag the question with up to 5 tags. If the user is updating a question, the form needs to be pre-populated with the existing data.
    """
    subject = forms.CharField(
        max_length=100, 
        required=True, 
        label='Enter your question heading here',  # Update the label here
        help_text='Enter a subject line for your question.'
    )
    content = QuillFormField()
    tags = forms.CharField(required=False)

    class Meta:
        """
        the Meta class is used to specify the model to which the form is associated and the fields from the model you want the form to include.
        """
        model = Question  # Specifies the model in models.py associated with this form
        fields = ['subject', 'content', 'tags']

    def clean_subject(self):
        print('cleaning subject')
        subject = self.cleaned_data.get('subject')
        if self.instance.pk:  # if this form is updating an existing instance
            print('checking if question with same subject exists')
            if Question.objects.filter(subject=subject).exclude(pk=self.instance.pk).exists(): # Check if a question with the same subject exists, excluding the current question
                print('question with same subject exists')
                print('raising error')
                raise forms.ValidationError('A question with this subject already exists.')
        else: # if this form is creating a new instance
            if Question.objects.filter(subject=subject).exists():
                raise forms.ValidationError('A question with this subject already exists.')
        return subject
  

    def clean_tags(self):
        print('cleaning tags')
        tags = self.cleaned_data.get('tags', '')
        print('saving cleaned tags', tags)
        return tags

    def save(self, *args, **kwargs):
        instance = super(QuestionForm, self).save(commit=False)
        # Save the instance to ensure it has an ID for many-to-many relationships
        instance.save()
        print('saving question', instance)

        # Handling tags here
        tags = self.cleaned_data.get('tags', '')
        tag_names = tags.split()  # Split the string into a list of tag names
        print(tag_names, '=tag_names after tag.split') # expecting ['tag1', 'tag2', 'tag3'] etc.

        # Clear existing tags first if needed, which is important when updating a question
        instance.tags.clear()

        # Add each tag individually
        for tag_name in tag_names:
            instance.tags.add(tag_name.strip())  # Ensure tag is stripped of extra whitespace

        print('instance.tags.all:', instance.tags.all()) 

        # If there are other many-to-many fields that need to be saved, call save_m2m() if necessary

        return instance


    def __init__(self, *args, **kwargs):
        # This is for checking if the form is bound to an existing instance, i.e. if the form is being used to update an existing question
        super(QuestionForm, self).__init__(*args, **kwargs)
        if self.instance.pk:  # Check if this form is bound to an existing instance
            self.fields['tags'].initial = ' '.join(tag.name for tag in self.instance.tags.all())
            print('tags initial:', self.fields['tags'].initial)

class AnswerForm(forms.ModelForm) :
    """
    Form for answering a question as seen in question_detail.html. The user can enter the main body of the answer with django_quill module. If the user is updating an answer, the form needs to be pre-populated with the existing data.
    """
    body = QuillFormField()

    class Meta: # Meta class is used to specify the model to which the form is associated
        model = Answer
        fields = ['body']
