import datetime

from django.conf import settings
from django.views.decorators.cache import cache_page

from app_utils.tools import render_response
from apps.theleague.models import League, Round


@cache_page(60 * 60)
def index(request):
    """ Display the current round """
    now = datetime.datetime.now()
    season = League.objects.get(pk=settings.LEAGUE_ID).current_season

    if season:
        rounds = season.round_set.filter(go_dead_date__gt=now).order_by(
                'go_live_date')[:1]

    current_round = rounds.get() if rounds else None

    return render_response(request, 'pages/index.html', {
        'current_round': current_round,
    })


@cache_page(60 * 60 * 24)
def rules(request):
    """ Display the rules. """
    return render_response(request, 'pages/rules.html', {})
