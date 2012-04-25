from django.contrib import admin

from apps.theleague.models import (Division, Game, League, Match, Round,
                                   Season, Team)


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
    list_display = ('player1', 'player2', 'date_created', 'date_modified')
    list_display_links = ('player1', 'player2',)
    list_filter = ('date_created', 'date_modified')
    save_on_top = True
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
    """ A class for the admin
    """
    list_display = ('name', 'short_name', 'go_live_date', 'go_dead_date',
                    'date_created', 'date_modified')
    list_display_links = ('name', 'go_live_date', 'go_dead_date')
    list_filter = ('date_created', 'date_modified')
    search_fields = ('name',)
    save_on_top = True
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
