"""
WSGI config for The Endless Nights Engine.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'endless_nights.settings')

application = get_wsgi_application()