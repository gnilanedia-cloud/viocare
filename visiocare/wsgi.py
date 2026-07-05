"""Configuration WSGI pour le projet VisioCare (utilisée par PythonAnywhere)."""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visiocare.settings')
application = get_wsgi_application()
