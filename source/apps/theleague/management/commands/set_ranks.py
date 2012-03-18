from django.core.management.base import BaseCommand

from apps.theleague.models import Game


class Command(BaseCommand):
    """ This goes through each game with a set winner that hasn't been ranked,
    and runs the ranking mechanism.
    """
    help = "Runs the ranking mechanism for any unranked games."

    def handle(self, *args, **options):
        for game in Game.objects.filter(ranked=False, winner__isnull=False):
            game.set_rank()
