"""
WSGI config for webapps project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapps.settings")

# application = get_wsgi_application()

env_variables_to_pass = ('GRUMBLR_SECRET_KEY')
def application(environ, start_response):
    if 'DJANGO_SETTINGS_MODULE' in environ:
        os.environ['DJANGO_SETTINGS_MODULE'] = environ['DJANGO_SETTINGS_MODULE']

    for var in env_variables_to_pass:
        os.environ[var] = environ.get(var, '')
    return get_wsgi_application()(environ, start_response)