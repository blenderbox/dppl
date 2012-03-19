import datetime

from django.core.management.base import BaseCommand

from apps.theleague.models import Match


class Command(BaseCommand):
    """ This goes through each unscored match and scores it if it adds up
    properly.
    """
    help = "Runs the match scoring mechanism for any unscored matches."

    def handle(self, *args, **options):
        today = datetime.date.today()
        matches = Match.objects.filter(
                team1_score__isnull=True,
                team2_score__isnull=True,
                round__go_live_date__lte=today,
                )

        for match in matches:
            match.set_score()
