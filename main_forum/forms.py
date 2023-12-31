from .models import Question, TeachingStandardTag, Answer
from django import forms
from django_summernote.widgets import SummernoteWidget




class QuestionForm(forms.ModelForm):
    """
    Form for asking a question. The user can enter a subject line and the main body of the question. They can also tag the question with up to 3 standards.


       The 8 UK Teaching Standards are:
    1. High Expectations
    2. Promoting Progress
    3. Subject Knowledge
    4. Planning
    5. Differentiation
    6. Assessment
    7. Behaviour Management
    8. Professionalism

    Parameters: The body can be no longer than 10000 characters. When choosing teacher standard, they can tag the question with up to 3 standards.
    """
    
    subject = forms.CharField(
        max_length=100, 
        required=True, 
        label='Enter your question heading here',  # Update the label here
        help_text='Enter a subject line for your question.'
    )
    content = forms.CharField(
        widget=SummernoteWidget(),
        max_length=10000, 
        required=True, 
        help_text='Enter the main body of your question.'
    ) # Use Summernote widget for content
    standards = forms.ModelMultipleChoiceField(
        queryset=TeachingStandardTag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text='Select the standard(s) for which you are asking the question.'
    )

    class Meta:
        """
        the Meta class is used to specify the model to which the form is associated and the fields from the model you want the form to include.
        """
        model = Question  # Specifies the model in models.py associated with this form
        fields = ['subject', 'content', 'standards']  # The fields from the model you want the form to include

class AnswerForm(forms.ModelForm) :
    class Meta: # Meta class is used to specify the model to which the form is associated
        model = Answer
        fields = ('body',)
        widgets = {
            'body': SummernoteWidget(),
        }
