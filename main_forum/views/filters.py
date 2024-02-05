# views/filters.py
# these views are for filtering the questions based on the tags, the user, and/ or the search query

from django.views.generic.list import ListView
from ..models import Question
from taggit.models import Tag

class FilterByTagView(ListView):
    model = Question
    template_name = 'filtered_questions.html'
    context_object_name = 'questions'
    print("FilterByTagView")

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        tag = Tag.objects.get(slug=tag_slug)
        return Question.objects.filter(tags__slug=tag_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs.get('tag_slug'))
        return context

