import os
import sys

path = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))

# make sure the current project is in PYTHONPATH
if path not in sys.path:
    sys.path.append(path)

# set the environment settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'source.settings')

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
