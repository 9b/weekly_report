import os
import sys

path = '/var/www'
if path not in sys.path:
    sys.path.append(path)


os.environ['DJANGO_SETTINGS_MODULE'] = 'weekly_report.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
