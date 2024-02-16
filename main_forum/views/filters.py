# views/filters.py
# these views are for filtering the questions based on the tags, the user, and/ or the search query

from django.views.generic.list import ListView
from ..models import Question
from django.shortcuts import get_object_or_404
from taggit.models import Tag

class FilterByTagView(ListView):
    model = Question
    template_name = 'filtered_questions.html'
    context_object_name = 'questions'

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        # Retrieve the Tag object by slug
        tag = get_object_or_404(Tag, slug=tag_slug)
        # Use TaggedItemManager's filter method to get questions tagged with the retrieved tag
        return Question.objects.filter(tags__slug=tag.slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('tag_slug')
        context['tag'] = get_object_or_404(Tag, slug=tag_slug)
        return context
