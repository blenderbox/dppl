from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('apps.theleague.views',
    # /schedule
    url(r'^schedule/$', 'schedule', name='theleague_schedule'),

    # /scoreboard
    url(r'^scoreboard/$', 'scoreboard', name='theleague_scoreboard'),

    # /teams/<team-slug>/<team-member-slug>/
    url(r'^teams/(?P<team_slug>[-\w]+)/(?P<team_member_slug>[-\w]+)/$',\
        'team_member', name="theleague_team_member"),

    # /teams/<team-slug>/
    url(r'^teams/(?P<team_slug>[-\w]+)/$', 'team', name="theleague_team"),

    # /teams
    url(r'^teams/$', 'team', name='theleague_teams'),
)
