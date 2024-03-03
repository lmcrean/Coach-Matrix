# views/filters.py
# these views are for filtering the questions based on the tags, the user, and/ or the search query

from django.views.generic.list import ListView
from ..models import Question
from django.shortcuts import get_object_or_404
from taggit.models import Tag, TaggedItem

class FilterByTagView(ListView):
    """
    This class will create a view for filtering questions by tag. It will display the questions associated with a specific tag in a list format that will be displayed in the filtered_questions.html template.
    """
    model = Question
    template_name = 'filtered_questions.html'
    context_object_name = 'questions'

    def get_queryset(self): # This method will return the queryset of questions associated with the tag, and is used to filter the questions by tag
        tag_slug = self.kwargs.get('tag_slug')
        tag = get_object_or_404(Tag, slug=tag_slug)
        # Use TaggedItem to query all items associated with the tag
        questions_ids = TaggedItem.objects.filter(tag_id=tag.id).values_list('object_id', flat=True)
        return Question.objects.filter(id__in=questions_ids) # Return the questions associated with the tag

    def get_context_data(self, **kwargs): # This method will return the context data for the template, and is used to pass the tag to the template.
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('tag_slug')
        context['tag'] = get_object_or_404(Tag, slug=tag_slug)
        return context 

