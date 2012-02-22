from django.contrib import admin

from apps.theleague.models import Division, League, Match, Season, Team


class DivisionAdmin(admin.ModelAdmin):
    """ A class for the admin
    """
    list_display = ('name', 'date_created', 'date_modified')
    list_display_links = ('name',)
    list_filter = ('date_created', 'date_modified')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    save_on_top = True
admin.site.register(Division, DivisionAdmin)


class LeagueAdmin(admin.ModelAdmin):
    """ A class for the admin
    """
    list_display = ('name', 'date_created', 'date_modified')
    list_display_links = ('name',)
    list_filter = ('date_created', 'date_modified')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    save_on_top = True
admin.site.register(League, LeagueAdmin)


class MatchAdmin(admin.ModelAdmin):
    """ A class for the admin
    """
    fieldsets = (
        (None, {'fields': ("date", "team1", "team1_score", "team2", "team2_score")}),
    )
    list_display = ('date', 'date_created', 'date_modified')
    list_display_links = ('date',)
    list_filter = ('date_created', 'date_modified')
    search_fields = ('date',)
    save_on_top = True
admin.site.register(Match, MatchAdmin)


class SeasonAdmin(admin.ModelAdmin):
    """ A class for the admin
    """
    list_display = ('name', 'date_created', 'date_modified')
    list_display_links = ('name',)
    list_filter = ('date_created', 'date_modified')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    save_on_top = True
admin.site.register(Season, SeasonAdmin)


class TeamAdmin(admin.ModelAdmin):
    """ A class for the admin
    """
    list_display = ('name', 'date_created', 'date_modified')
    list_display_links = ('name',)
    list_filter = ('date_created', 'date_modified')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    save_on_top = True
admin.site.register(Team, TeamAdmin)
