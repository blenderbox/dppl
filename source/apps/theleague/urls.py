from django.contrib import admin
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('apps.theleague.views',
    # /schedule
    url(r'^schedule/$', 'schedule', name='theleague_schedule'),
    # /scoreboard
    url(r'^scoreboard/$', 'scoreboard', name='theleague_scoreboard'),
    # /teams/<team-slug>/
    url(r'^teams/(?P<team_slug>[-\w]+)/$', 'team', name="theleague_team"),
    # /teams
    url(r'^teams/$', 'teams', name='theleague_teams'),
)
