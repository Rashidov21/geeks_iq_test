"""
WSGI config for geeks_iq project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geeks_iq.settings')

application = get_wsgi_application()
