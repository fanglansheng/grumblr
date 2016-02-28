import os
import sys
sys.path = ['/var/www/grumblr']+sys.path
os.environ['DJANGO_SETTINGS-MODULE'] = 'grumblr.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

