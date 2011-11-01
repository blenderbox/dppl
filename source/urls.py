from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template


admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^news/', include('news.foo.urls')),

    (r'^commander/', include(admin.site.urls)),
)

if getattr(settings, "DEBUG", False):
    # Load template urls for reference
    h = lambda x: direct_to_template(template="html/%s" % x)
    urlpatterns = patterns('',
        url(r"^html/(?P<template>.*)$", h),
    ) + urlpatterns

if getattr(settings, "LOCAL_SERVE", False):
    urlpatterns = patterns('django.views.static',
        url(r"^%s(?P<path>.*)$" % settings.MEDIA_URL.lstrip('/'), "serve", {
            'document_root': settings.MEDIA_ROOT, 'show_indexes': True,
        }),
    ) + staticfiles_urlpatterns() + urlpatterns
