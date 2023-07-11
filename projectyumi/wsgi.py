"""
WSGI config for projectyumi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectyumi.settings')

application = get_wsgi_application()

<<<<<<< HEAD
app = application
=======
app = application
>>>>>>> 97e021bca1a47f6285d091b31e3120f96af7aa8d
