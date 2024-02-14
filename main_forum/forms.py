from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Question, Tag, Answer
from django_quill.forms import QuillFormField
from taggit.forms import TagField
from django.contrib.auth.forms import PasswordChangeForm



class QuestionForm(forms.ModelForm):
    """
    Form for asking a question. The user can enter a subject line and the main body of the question. They can also tag the question with up to 5 tags. If the user is updating a question, the form needs to be pre-populated with the existing data.
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
        print('saving question')
        instance = super(QuestionForm, self).save(commit=False)
        # Do not commit yet, need to save m2m relations (tags) after the instance is saved
        instance.save()
        # Handling tags here
        tags = self.cleaned_data.get('tags', '')
        tag_names = tags.split()  # Split the string into a list of tag names
        instance.tags.set(tag_names, clear=True) # Set the tags for the instance
        print('instance.tags.all:', instance.tags.all())
        return instance

    def __init__(self, *args, **kwargs):
        # This is for checking if the form is bound to an existing instance, i.e. if the form is being used to update an existing question
        super(QuestionForm, self).__init__(*args, **kwargs)
        if self.instance.pk:  # Check if this form is bound to an existing instance
            self.fields['tags'].initial = ' '.join(tag.name for tag in self.instance.tags.all())
            print('tags initial:', self.fields['tags'].initial)

class AnswerForm(forms.ModelForm) :
    body = QuillFormField()

    class Meta: # Meta class is used to specify the model to which the form is associated
        model = Answer
        fields = ['body']

class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Update Profile'))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('A user with that email already exists.')
        return email

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_action = 'change_password'
        self.helper.add_input(Submit('submit', 'Change Password'))