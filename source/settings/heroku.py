from os import environ
from sys import exc_info
from urlparse import urlparse, uses_netloc

from S3 import CallingFormat

from defaults import *


env = lambda e, d: environ.get(e, d)

DEBUG = False
HEROKU = True
LOCAL_SERVE = False
TEMPLATE_DEBUG = True

# Temporarily overriding admins for error mailing
ADMINS = MANAGERS = (
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
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': url.path[1:],
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port,
        }

except:
    print "Unexpected error:", exc_info()

SOUTH_DATABASE_ADAPTERS = {
    'default': 'south.db.postgresql_psycopg2',
}

INSTALLED_APPS += (
    'debug_toolbar',
    'johnny_panel',
    'storages',
)

# Memcachedddd
if 'MEMCACHE_SERVERS' in environ:
    MIDDLEWARE_CLASSES = (
        # Cache Update
        'django.middleware.cache.UpdateCacheMiddleware',
        'johnny.middleware.LocalStoreClearMiddleware',
        'johnny.middleware.QueryCacheMiddleware',
    ) + MIDDLEWARE_CLASSES + (
        # Cache Fetch
        'django.middleware.cache.FetchFromCacheMiddleware',
    )

    cache_common = {
        'LOCATION': "%s:11211" % env('MEMCACHE_SERVERS', ''),
        'username': env('MEMCACHE_USERNAME', ''),
        'password': env('MEMCACHE_PASSWORD', ''),
        'BINARY': True,
        'OPTIONS': {
            'tcp_nodelay': True,
            'ketama': True,
        },
    }

    default_cache = {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'TIMEOUT': 300,
    }
    default_cache.update(cache_common)

    johnny_cache = {
        'BACKEND': 'johnny.backends.memcached.MemcachedCache',
        'JOHNNY_CACHE': True,
    }
    johnny_cache.update(cache_common)

    CACHES = {'default': default_cache, 'johnny': johnny_cache}

# Only cache for anonymous users
JOHNNY_MIDDLEWARE_KEY_PREFIX = 'johnny'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 300

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

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
    'debug_toolbar.panels.cache.CacheDebugPanel',
    'johnny_panel.panel.JohnnyPanel',
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
