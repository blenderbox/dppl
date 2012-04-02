from os import environ
from sys import exc_info
from urlparse import urlparse, uses_netloc

from S3 import CallingFormat

from defaults import *


# Bump

env = lambda e, d: environ[e] if e in environ else d

# DEBUG = True
DEBUG = False
HEROKU = True
LOCAL_SERVE = False
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

INSTALLED_APPS += ('storages',)

# Memcachedddd
CACHES = {
    'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'LOCATION': 'localhost:11211',
        'TIMEOUT': 300,
        'BINARY': True,
        'OPTIONS': {
                'tcp_nodelay': True,
                'ketama': True,
        }
    },
}
# Only cache for anonymous users
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

# DB backed sessions for testing since cache dumps itself
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN
AWS_HEADERS = {
    'x-amz-acl': 'public-read',
    'Expires': 'Sat, 30 Oct 2010 20:00:00 GMT',
    'Cache-Control': 'public, max-age=3153600',
}
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME', '')
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', '')
AWS_QUERYSTRING_AUTH = False
# AWS_IS_GZIPPED = True
COMPRESS_CSS_FILTERS = [
        'compressor.filters.css_default.CssAbsoluteFilter',
        'compressor.filters.cssmin.CSSMinFilter',
    ]

STATIC_URL = 'http://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
COMPRESS_ROOT = get_path(PROJECT_DIR, "../public")
COMPRESS_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
COMPRESS_OFFLINE = True
