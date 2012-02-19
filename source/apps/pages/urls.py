from django.contrib import admin
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('apps.pages.views',
    # /
    url(r'^$', 'index', name='pages_index'),
)
