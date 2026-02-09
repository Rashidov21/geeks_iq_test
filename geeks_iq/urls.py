"""
URL configuration for Geeks Andijan IQ Test.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('iq_test.urls')),
]
