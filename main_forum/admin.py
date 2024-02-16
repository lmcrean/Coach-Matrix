from django.contrib import admin
from .models import Question, Answer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_on', 'net_votes')
    search_fields = ['title', 'content', 'tags__name']
    list_filter = ('status', 'created_on', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)  # This will add a widget to manage ManyToMany relationship with tags.

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):

    list_display = ('name', 'body', 'question', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_answers']

    def approve_answers(self, request, queryset):
        queryset.update(approved=True)
