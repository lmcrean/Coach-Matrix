# views/filters.py
# these views are for filtering the questions based on the tags, the user, and/ or the search query

from django.views.generic.list import ListView
from ..models import Question
from django.shortcuts import get_object_or_404
from taggit.models import Tag, TaggedItem

class FilterByTagView(ListView):
    model = Question
    template_name = 'filtered_questions.html'
    context_object_name = 'questions'

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        tag = get_object_or_404(Tag, slug=tag_slug)
        # Use TaggedItem to query all items associated with the tag
        questions_ids = TaggedItem.objects.filter(tag_id=tag.id).values_list('object_id', flat=True)
        print(questions_ids)
        return Question.objects.filter(id__in=questions_ids)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('tag_slug')
        context['tag'] = get_object_or_404(Tag, slug=tag_slug)
        return context

