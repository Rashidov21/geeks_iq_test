"""
Database models for Geeks Andijan IQ Test.
Supports: text, Raven's matrices, abstract reasoning, visual puzzles.
"""

from django.db import models


class Question(models.Model):
    """IQ test question - text, Raven's, abstract, or visual type."""

    QUESTION_TYPE_CHOICES = [
        ('text', 'Matnli savol'),
        ('raven', "Raven matritsasi"),
        ('abstract', 'Abstract reasoning'),
        ('visual', 'Visual puzzle'),
    ]

    DIFFICULTY_CHOICES = [
        ('easy', 'Oson'),
        ('medium', "O'rta"),
        ('hard', 'Qiyin'),
    ]

    ANSWER_CHOICES = [
        ('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'),
        ('e', 'E'), ('f', 'F'), ('g', 'G'), ('h', 'H'),
    ]

    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPE_CHOICES,
        default='text',
        verbose_name='Savol turi'
    )
    text = models.TextField(verbose_name='Savol matni', blank=True)
    image = models.ImageField(
        upload_to='questions/',
        blank=True,
        null=True,
        verbose_name='Savol rasmi (Raven/Visual uchun)'
    )
    option_a = models.CharField(max_length=500, blank=True)
    option_b = models.CharField(max_length=500, blank=True)
    option_c = models.CharField(max_length=500, blank=True)
    option_d = models.CharField(max_length=500, blank=True)
    option_e = models.CharField(max_length=500, blank=True)
    option_f = models.CharField(max_length=500, blank=True)
    option_g = models.CharField(max_length=500, blank=True)
    option_h = models.CharField(max_length=500, blank=True)
    option_a_image = models.ImageField(upload_to='options/', blank=True, null=True)
    option_b_image = models.ImageField(upload_to='options/', blank=True, null=True)
    option_c_image = models.ImageField(upload_to='options/', blank=True, null=True)
    option_d_image = models.ImageField(upload_to='options/', blank=True, null=True)
    option_e_image = models.ImageField(upload_to='options/', blank=True, null=True)
    option_f_image = models.ImageField(upload_to='options/', blank=True, null=True)
    option_g_image = models.ImageField(upload_to='options/', blank=True, null=True)
    option_h_image = models.ImageField(upload_to='options/', blank=True, null=True)
    correct_answer = models.CharField(
        max_length=1,
        choices=ANSWER_CHOICES
    )
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='medium'
    )
    is_active = models.BooleanField(default=True, verbose_name='Faol')

    class Meta:
        ordering = ['id']
        verbose_name = 'Savol'
        verbose_name_plural = 'Savollar'

    def __str__(self):
        return self.text[:50] + '...' if self.text and len(self.text) > 50 else (self.text or f'{self.get_question_type_display()} #{self.id}')

    def get_options_list(self):
        """Return list of (letter, text_or_none, image_or_none) for non-empty options."""
        letters = 'abcdefgh'
        result = []
        for i, letter in enumerate(letters):
            text = getattr(self, f'option_{letter}', None) or ''
            img = getattr(self, f'option_{letter}_image', None)
            if text or (img and img.name):
                result.append((letter, text.strip() or None, img))
        return result


class UserResult(models.Model):
    """Student test result - no login required."""

    GENDER_CHOICES = [
        ('M', 'Erkak'),
        ('F', 'Ayol'),
    ]

    name = models.CharField(max_length=100, verbose_name='Ism')
    age = models.IntegerField(verbose_name='Yosh')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Jinsi')
    phone = models.CharField(max_length=20, verbose_name='Telefon')
    score = models.IntegerField(verbose_name='Ball')
    correct_count = models.PositiveIntegerField(default=0, verbose_name='To\'g\'ri javoblar')
    total_questions = models.PositiveIntegerField(default=0, verbose_name='Jami savollar')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Natija'
        verbose_name_plural = 'Natijalar'

    def __str__(self):
        return f"{self.name} - {self.score} ball"


class TestSession(models.Model):
    """Optional: tracks individual test sessions."""

    user_result = models.ForeignKey(
        UserResult,
        on_delete=models.CASCADE,
        related_name='sessions',
        null=True,
        blank=True
    )
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    time_spent = models.IntegerField(null=True, blank=True, help_text='Seconds')

    class Meta:
        ordering = ['-started_at']
        verbose_name = 'Test sessiyasi'
        verbose_name_plural = 'Test sessiyalari'
