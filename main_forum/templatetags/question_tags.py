# main_forum/templatetags/question_tags.py

# this is a custom template tag that will be used to check if a question is
# bookmarked by a user.

from django import template
from main_forum.models import Bookmark

register = template.Library()


@register.filter
def is_bookmarked_by(question, user):
    return Bookmark.objects.filter(question=question, user=user).exists()
