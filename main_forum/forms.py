from .models import Question, TeachingStandardTag, Answer
from django import forms
from ckeditor.widgets import CKEditorWidget
from django_quill.forms import QuillFormField


class QuestionForm(forms.ModelForm):
    """
    Form for asking a question. The user can enter a subject line and the main body of the question. They can also tag the question with up to 3 standards.
    """
    subject = forms.CharField(
        max_length=100, 
        required=True, 
        label='Enter your question heading here',  # Update the label here
        help_text='Enter a subject line for your question.'
    )
    content = QuillFormField()

    class Meta:
        """
        the Meta class is used to specify the model to which the form is associated and the fields from the model you want the form to include.
        """
        model = Question  # Specifies the model in models.py associated with this form
        fields = ['subject', 'content']  

class AnswerForm(forms.ModelForm) :
    body = QuillFormField()

    class Meta: # Meta class is used to specify the model to which the form is associated
        model = Answer
        fields = ['body']
