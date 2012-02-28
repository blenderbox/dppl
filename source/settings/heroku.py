from os import environ
from sys import exc_info
from urlparse import urlparse, uses_netloc

from settings.defaults import *


DEBUG = True
LOCAL_SERVE = True
TEMPLATE_DEBUG = True

# To run a testing server:
# python -m smtpd -n -c DebuggingServer localhost:1025
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025

uses_netloc.append('postgres')
uses_netloc.append('mysql')

try:
    if 'DATABASE_URL' in environ:
        url = urlparse(environ['DATABASE_URL'])
        DATABASES['default'] = {
            'NAME': url.path[1:],
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port,
        }

        DATABASES['default']['ENGINE'] = 'django.db.backends.'
        if url.scheme == 'postgres':
            DATABASES['default']['ENGINE'] += 'postgresql_psycopg2'
        elif url.scheme == 'mysql':
            DATABASES['default']['ENGINE'] += 'mysql'
except:
    print "Unexpected error:", exc_info()

# Dummy cache for dev
CACHES = {
    'default': {
        'BACKEND': "django.core.cache.backends.dummy.DummyCache",
    },
}

# DB backed sessions for testing since cache dumps itself
SESSION_ENGINE = "django.contrib.sessions.backends.db"
