"""
URL routing for IQ Test app.
"""

from django.urls import path
from . import views

app_name = 'iq_test'

urlpatterns = [
    # Student flow
    path('', views.landing, name='landing'),
    path('info/', views.student_info, name='student_info'),
    path('test/', views.start_test, name='start_test'),
    path('api/questions/', views.get_questions, name='get_questions'),
    path('api/submit/', views.submit_test, name='submit_test'),
    path('results/', views.results, name='results'),
    path('results/<int:result_id>/', views.results, name='results_detail'),
]
