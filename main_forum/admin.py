from django.contrib import admin
from .models import Question, Answer, TeachingStandardTag

@admin.register(TeachingStandardTag)
class TeachingStandardTagAdmin(admin.ModelAdmin):
    """
    The 8 UK Teaching Standards are:
    1. High Expectations
    2. Promoting Progress
    3. Subject Knowledge
    4. Planning
    5. Differentiation
    6. Assessment
    7. Behaviour Management
    8. Professionalism
    """
    list_display = ('name',)  # This will display the name of the standard in the admin panel
    

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    list_filter = ('status', 'created_on')
    prepopulated_fields = {'slug': ('title',)}
    # filter_horizontal = ('standards',)  # This will add a nice widget to manage ManyToMany relationship

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):

    list_display = ('name', 'body', 'question', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_answers']

    def approve_answers(self, request, queryset):
        queryset.update(approved=True)
