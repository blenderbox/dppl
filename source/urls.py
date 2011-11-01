from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template


admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^news/', include('news.foo.urls')),

    (r"^commander/", include(admin.site.urls)),
)

if getattr(settings, "DEBUG", False):
    # Load template urls for reference
    def h(*args, **kwargs):
        t = "%s/%s" % (kwargs['base'], kwargs['template'])
        if t.endswith('/'):
            t = "%sindex.html" % t
        kwargs['template'] = t
        return direct_to_template(*args, **kwargs)

    urlpatterns = patterns('',
        url(r"^(?P<base>html)/(?P<template>.*)$", h),
    ) + urlpatterns

if getattr(settings, "LOCAL_SERVE", False):
    urlpatterns = patterns('django.views.static',
        url(r"^%s(?P<path>.*)$" % settings.MEDIA_URL.lstrip('/'), "serve", {
            'document_root': settings.MEDIA_ROOT, 'show_indexes': True,
        }),
    ) + staticfiles_urlpatterns() + urlpatterns
