from django.contrib import admin
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('apps.homepage.views',
    # /
    url(r'^$', 'index', name='homepage_index'),
)
