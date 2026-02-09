"""
Database models for Geeks Andijan IQ Test.
"""

from django.db import models


class Question(models.Model):
    """IQ test question with multiple choice answers."""

    DIFFICULTY_CHOICES = [
        ('easy', 'Oson'),
        ('medium', "O'rta"),
        ('hard', 'Qiyin'),
    ]

    text = models.TextField(verbose_name='Savol matni')
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255, blank=True)
    option_d = models.CharField(max_length=255, blank=True)
    correct_answer = models.CharField(
        max_length=1,
        choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')]
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
        return self.text[:50] + '...' if len(self.text) > 50 else self.text


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
