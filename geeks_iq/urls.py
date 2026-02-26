"""
URL configuration for Geeks Andijan IQ Test.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('iq_test.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'iq_test.views.page_not_found_view'
handler500 = 'iq_test.views.server_error_view'
