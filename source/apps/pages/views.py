import datetime

from django.conf import settings

from app_utils.tools import render_response
from apps.theleague.models import League, Round


def index(request):
    """ Display the current round """
    now = datetime.datetime.now()
    season = League.objects.get(pk=settings.LEAGUE_ID).current_season

    if season is not None:
        rounds = season.round_set.filter(go_dead_date__gt=now).order_by(
                'go_live_date')[:1]

    try:
        _round = rounds.get()
    except Round.DoesNotExist:
        _round = None

    return render_response(request, 'pages/index.html', {
        'current_round': _round,
        })


def rules(request):
    """ Display the rules. """
    return render_response(request, 'pages/rules.html', {})
