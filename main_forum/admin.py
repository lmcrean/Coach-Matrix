# main_forum/admin.py

# The admin settings will include the QuestionAdmin and AnswerAdmin classes,
# which will be used to customize the admin interface for the Question and
# Answer models.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Question, Answer, ReputationPoints


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'UserProfile'
    fields = ('reputation',)  # Display only the reputation field


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )


# Unregister the default User admin and register the new UserAdmin class
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('subject', 'author', 'status', 'created_on', 'net_votes')
    search_fields = ['subject', 'content', 'tags__name']
    list_filter = ('status', 'created_on')
    prepopulated_fields = {'slug': ('subject',)}
    filter_horizontal = ('tags',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):

    list_display = ('author', 'body', 'question', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_answers']

    def approve_answers(self, request, queryset):
        queryset.update(approved=True)


@admin.register(ReputationPoints)
class ReputationPointsAdmin(admin.ModelAdmin):
    list_display = ('user', 'reputation', 'date_awarded')
    search_fields = ('user__username', 'reputation')
    list_filter = ('date_awarded',)
