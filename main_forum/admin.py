# main_forum/admin.py

# The admin settings will include the QuestionAdmin and AnswerAdmin classes, which will be used to customize the admin interface for the Question and Answer models.

from django.contrib import admin
from .models.question_model import Question
from .models.answer_model import Answer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('subject', 'author', 'status', 'created_on', 'net_votes')
    search_fields = ['subject', 'content', 'tags__name']
    list_filter = ('status', 'created_on')
    prepopulated_fields = {'slug': ('subject',)}
    filter_horizontal = ('tags',)  # This will add a widget to manage ManyToMany relationship with tags.

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):

    list_display = ('name', 'body', 'question', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_answers']

    def approve_answers(self, request, queryset):
        queryset.update(approved=True)
