"""
WSGI config for SchoolLib project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application
import os
import dotenv
dotenv.read_dotenv(os.path.join(
    os.path.dirname(os.path.dirname(__file__)), '.env'))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SchoolLib.settings')

application = get_wsgi_application()
