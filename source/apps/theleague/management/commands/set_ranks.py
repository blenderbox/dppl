import datetime

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.theleague.models import Game


class Command(BaseCommand):
    """ This goes through each game with a set winner that hasn't been ranked,
    and runs the ranking mechanism.

    If this is running on Heroku (settings.HEROKU = True), we will make sure
    that we only run the rankings on rounds which have ended.
    """
    help = "Runs the ranking mechanism for any unranked games."

    def handle(self, *args, **options):
        games = Game.objects.filter(ranked=False, winner__isnull=False)

        if getattr(settings, 'HEROKU', False):
            games = games.filter(
                    match__round__go_dead_date__lte=datetime.datetime.now())

        for game in games:
            game.set_rank()
