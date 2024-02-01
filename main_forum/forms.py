from .models import Question, Tag, Answer
from django import forms
from ckeditor.widgets import CKEditorWidget
from django_quill.forms import QuillFormField
from taggit.forms import TagField


class QuestionForm(forms.ModelForm):
    """
    Form for asking a question. The user can enter a subject line and the main body of the question. They can also tag the question with up to 5 tags.
    """
    subject = forms.CharField(
        max_length=100, 
        required=True, 
        label='Enter your question heading here',  # Update the label here
        help_text='Enter a subject line for your question.'
    )
    content = QuillFormField()
    tags = TagField(
        label='Enter up to 5 tags for your question', 
        help_text='Enter up to 5 tags for your question. Separate tags with a comma.',
        required=True
    )

    class Meta:
        """
        the Meta class is used to specify the model to which the form is associated and the fields from the model you want the form to include.
        """
        model = Question  # Specifies the model in models.py associated with this form
        fields = ['subject', 'content', 'tags']  

    def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        instance.save()
        # If you're not using django-taggit and have a custom way to handle tags
        tags = self.cleaned_data.get('tags')
        if tags:
            # Process the tags string and save each tag to the instance
            for tag_name in tags.split(','):
                tag, created = TagModel.objects.get_or_create(name=tag_name.strip())
                instance.tags.add(tag)
        instance.save()
        return instance

class AnswerForm(forms.ModelForm) :
    body = QuillFormField()

    class Meta: # Meta class is used to specify the model to which the form is associated
        model = Answer
        fields = ['body']
