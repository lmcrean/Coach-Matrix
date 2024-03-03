# main_forum/forms/question_form.py

# This file contains the form for the Question model. The QuestionForm class will be used to create and update questions in the forum.

from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from ..models import Question, Answer
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

    print('QuestionForm') 
    print('content:', content)

    class Meta:
        """
        the Meta class is used to specify the model to which the form is associated and the fields from the model you want the form to include.
        """
        model = Question  # Specifies the model in models.py associated with this form
        fields = ['subject', 'content', 'tags']
        print('Meta fields:', fields) 

    def clean_subject(self):
        print('cleaning subject') # PASS
        subject = self.cleaned_data.get('subject')
        if self.instance.pk:  # if this form is updating an existing instance
            print('checking if question with same subject exists') # FAIL
            if Question.objects.filter(subject=subject).exclude(pk=self.instance.pk).exists(): # Check if a question with the same subject exists, excluding the current question
                print('question with same subject exists')
                print('raising error')
                raise forms.ValidationError('A question with this subject already exists.')
        else: # if this form is creating a new instance
            if Question.objects.filter(subject=subject).exists():
                raise forms.ValidationError('A question with this subject already exists.')
        return subject
  

    def clean_tags(self):
        print('cleaning tags') # PASS
        tags = self.cleaned_data.get('tags', '')
        print('saving cleaned tags', tags) # PASS
        return tags

    def save(self, *args, **kwargs):
        instance = super(QuestionForm, self).save(commit=False)
        # Save the instance to ensure it has an ID for many-to-many relationships
        instance.save()
        print('saving question', instance) # PASS

        # Handling tags here
        tags = self.cleaned_data.get('tags', '')
        tag_names = tags.split()  # Split the string into a list of tag names
        print('tag_names after tag.split', tag_names) # expecting ['tag1', 'tag2', 'tag3'] etc. PASS 

        # Clear existing tags first if needed, which is important when updating a question
        instance.tags.clear()

        # Add each tag individually
        for tag_name in tag_names:
            instance.tags.add(tag_name.strip())  # Ensure tag is stripped of extra whitespace

        print('instance.tags.all:', instance.tags.all()) # PASS <QuerySet [<Tag: tag1>, <Tag: tag2>, <Tag: tag3>]> etc.

        if self.instance.pk:
            # If this is an update, save the instance again
            instance.save()  # Save the instance again to save the many-to-many relationships
            print('instance saved:', instance)

        return instance


    def __init__(self, *args, **kwargs):
        """
        This is for checking if the form is bound to an existing instance, i.e. if the form is being used to update an existing question.

        self.fields['tags'].widget.attrs['id'] = 'id_tags' is used to add an id to the tags field so that it can be targeted by JavaScript.

        If the form is bound to an existing instance, pre-populate the tags field with the existing tags.
        """
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['tags'].widget.attrs['id'] = 'id_tags'  

        if self.instance.pk: 
            self.fields['tags'].initial = ' '.join(tag.name for tag in self.instance.tags.all()) # Pre-populate the tags field with the existing tags
            print('tags initial:', self.fields['tags'].initial) # PASS? tags initial: tag1 tag2 tag3