from os import environ
from sys import exc_info
from urlparse import urlparse, uses_netloc

from S3 import CallingFormat

from defaults import *


env = lambda e, d: environ[e] if e in environ else d

# DEBUG = True
DEBUG = False
HEROKU = True
LOCAL_SERVE = False
TEMPLATE_DEBUG = True

# Temporarily overriding admins for error mailing
ADMINS = (
    ("Damon Jablons", 'djablons@blenderbox.com'),
)


# Email Settings
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = env('SENDGRID_USERNAME', '')
EMAIL_HOST_PASSWORD = env('SENDGRID_PASSWORD', '')
EMAIL_SUBJECT_PREFIX = "[ pxlpng.com ] "
EMAIL_USE_TLS = True
SERVER_EMAIL = env('SENDGRID_USERNAME', '')


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

INSTALLED_APPS += (
    'debug_toolbar',
    'storages',
)
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

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


# Debug Toolbar
def show_toolbar(request):
    if 'debug' in request.GET:
        on = request.GET.get('debug') == "on"
        request.session['show_toolbar'] = on
    elif 'show_toolbar' in request.session:
        on = request.session['show_toolbar']
    else:
        on = False
        request.session['show_toolbar'] = on

    return not request.path.startswith('commander') and on

INTERNAL_IPS = ('64.21.121.50',)
DEBUG_TOOLBAR_PANELS = (
    # 'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
    'EXTRA_SIGNALS': ['myproject.signals.MySignal'],
    'HIDE_DJANGO_SQL': False,
    # 'TAG': 'div',
}

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
