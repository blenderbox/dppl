from django.conf import settings
from django.contrib import admin

from apps.theleague.models import (Division, Game, League, Match, Round,
                                   Season, Team, current_season)


class DivisionAdmin(admin.ModelAdmin):
    """ A class for the admin """
    list_display = ('name', 'date_created', 'date_modified')
    list_display_links = ('name',)
    list_filter = ('date_created', 'date_modified')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    save_on_top = True
admin.site.register(Division, DivisionAdmin)


class GameInline(admin.StackedInline):
    extra = 4
    max_num = 4
    model = Game


class RoundInline(admin.StackedInline):
    extra = 3
    model = Round


class GameAdmin(admin.ModelAdmin):
    """ A class for the admin """
    list_display = ('player1', 'player2', 'team1', 'team2', 'date_created',
                    'date_modified')
    list_display_links = ('player1', 'player2',)
    list_filter = ('match__round__season', 'match__team1', 'match__team2',
                   'match__round', 'date_created', 'date_modified')
    save_on_top = True

    def team1(self, obj):
        return obj.match.team1.name

    def team2(self, obj):
        return obj.match.team2.name
admin.site.register(Game, GameAdmin)


class LeagueAdmin(admin.ModelAdmin):
    """ A class for the admin """
    list_display = ('name', 'date_created', 'date_modified')
    list_display_links = ('name',)
    list_filter = ('date_created', 'date_modified')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    save_on_top = True
admin.site.register(League, LeagueAdmin)


class MatchAdmin(admin.ModelAdmin):
    """ A class for the admin """
    fieldsets = (
        (None, {'fields': ('round', 'division', 'team1', 'team1_score',
            'team2', 'team2_score')}),
    )
    list_display = ('team1', 'team2', 'round', 'complete', 'date_created',
                    'date_modified')
    list_display_links = ('round',)
    list_filter = ('round', 'date_created', 'date_modified')
    search_fields = ('round',)
    save_on_top = True
    inlines = [GameInline]
admin.site.register(Match, MatchAdmin)


class RoundAdmin(admin.ModelAdmin):
    """ A class for the admin. """
    list_display = ('name', 'season', 'short_name', 'go_live_date',
                    'go_dead_date', 'date_created', 'date_modified')
    list_display_links = ('name', 'go_live_date', 'go_dead_date')
    list_filter = ('season', 'date_created', 'date_modified')
    search_fields = ('name',)
    save_on_top = True

    def changelist_view(self, request, extra_context=None):
        """ Sets the currents season to be the default filter. """
        meta = request.META
        bits = meta.get('HTTP_REFERER', '').split(meta.get('PATH_INFO', ''))
        season = current_season(settings.LEAGUE_ID)

        if season and not bits[-1].startswith('?'):
            query = request.GET.copy()
            query['season__id__exact'] = season.id
            request.GET = query
            request.META['QUERY_STRING'] = request.GET.urlencode()

        return super(RoundAdmin, self).changelist_view(
            request, extra_context=extra_context
        )

admin.site.register(Round, RoundAdmin)


class SeasonAdmin(admin.ModelAdmin):
    """ A class for the admin
    """
    list_display = ('name', 'date_created', 'date_modified')
    list_display_links = ('name',)
    list_filter = ('date_created', 'date_modified')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    save_on_top = True

    inlines = [
        RoundInline,
    ]
admin.site.register(Season, SeasonAdmin)


class TeamAdmin(admin.ModelAdmin):
    """ A class for the admin
    """
    list_display = ('name', 'division', 'date_created', 'date_modified')
    list_display_links = ('name',)
    list_filter = ('date_created', 'date_modified')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    save_on_top = True
admin.site.register(Team, TeamAdmin)
