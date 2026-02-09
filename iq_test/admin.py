"""
Django admin configuration for IQ Test.
"""

from django.contrib import admin
from .models import Question, UserResult, TestSession


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question_type', 'text_short', 'difficulty', 'correct_answer', 'is_active']
    list_filter = ['question_type', 'difficulty', 'is_active']
    search_fields = ['text']
    list_editable = ['is_active']

    fieldsets = (
        (None, {
            'fields': ('question_type', 'text', 'image', 'correct_answer', 'difficulty', 'is_active')
        }),
        ('Matnli variantlar (A-D)', {
            'fields': ('option_a', 'option_b', 'option_c', 'option_d'),
            'description': 'Matnli savollar uchun'
        }),
        ('Qo\'shimcha variantlar (E-H, Raven uchun)', {
            'fields': ('option_e', 'option_f', 'option_g', 'option_h'),
            'classes': ('collapse',)
        }),
        ('Rasmli variantlar (Raven/Visual)', {
            'fields': ('option_a_image', 'option_b_image', 'option_c_image', 'option_d_image',
                       'option_e_image', 'option_f_image', 'option_g_image', 'option_h_image'),
            'classes': ('collapse',)
        }),
    )

    def text_short(self, obj):
        t = obj.text or obj.get_question_type_display() or ''
        return (t[:60] + '...') if len(t) > 60 else t

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
