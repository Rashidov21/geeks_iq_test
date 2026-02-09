"""
Django admin configuration for IQ Test.
"""

from django.contrib import admin
from .models import Question, UserResult, TestSession


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'text_short', 'difficulty', 'correct_answer', 'is_active']
    list_filter = ['difficulty', 'is_active']
    search_fields = ['text']
    list_editable = ['is_active']

    def text_short(self, obj):
        return obj.text[:60] + '...' if len(obj.text) > 60 else obj.text

    text_short.short_description = 'Savol'


@admin.register(UserResult)
class UserResultAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'gender', 'score', 'created_at']
    list_filter = ['gender', 'created_at']
    search_fields = ['name', 'phone']
    readonly_fields = ['created_at']


@admin.register(TestSession)
class TestSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_result', 'started_at', 'finished_at', 'time_spent']
    list_filter = ['started_at']
