from django.contrib import admin
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('apps.pages.views',
    # /rules
    url(r'^rules/$', 'rules', name='pages_rules'),
    # /
    url(r'^$', 'index', name='pages_index'),
)
