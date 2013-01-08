from defaults import *
from passwords import DB_USERNAME, DB_PASSWORD


DEBUG = False
HEROKU = True
LOCAL_SERVE = False
TEMPLATE_DEBUG = True

# Temporarily overriding admins for error mailing
ADMINS = (
    ("Damon Jablons", 'djablons@blenderbox.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pxlpng',
        'USER': DB_USERNAME,
        'PASSWORD': DB_PASSWORD,
    },
}

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
        'LOCATION': "127.0.0.1:11211",
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
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

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]

COMPRESS_ROOT = get_path(PROJECT_DIR, "../public")
