from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.abstract.models import CommonModel
from apps.accounts.elo import rank

from datetime import datetime


class Division(CommonModel):
    """ The division.  Right now, there are two, Honey and Badger.
    """
    name = models.CharField(_("Name"), max_length=255)
    # Leagues can have divisions w/ the same name
    slug = models.SlugField(_("Slug"), max_length=255)

    # Relations
    league = models.ForeignKey("League")

    class Meta:
        ordering = ("name",)

    def __unicode__(self):
        return self.name


class Game(CommonModel):
    """ The game.
    """
    WINNER_CHOICES = ((1, "Player 1",), (2, "Player 2"),)

    winner = models.CharField(_("Winner"), choices=WINNER_CHOICES,
            max_length=1, null=True, blank=True)
    # Relations
    match = models.ForeignKey("Match")
    player1 = models.ForeignKey(User, related_name="user1")
    player2 = models.ForeignKey(User, related_name="user2")

    def set_rank(self):
        """ This will rank players one and two based on the outcome. """
        if self.winner == 1:
            self.player1, self.player2 = rank(self.player1, self.player2)
        else:
            self.player2, self.player1 = rank(self.player2, self.player1)
        self.player1.save()
        self.player2.save()


class League(CommonModel):
    """  This is the league.  It won't really get used except if we go global.
         Which we will.
    """
    name = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(_("Slug"), max_length=255, unique=True)

    class Meta:
        ordering = ("name",)

    def __unicode__(self):
        return self.name


class Season(CommonModel):
    """ The season.
    """
    name = models.CharField(_("Name"), max_length=255)
    # Don't make this unique because leagues can have seasons w/ the same name.
    slug = models.SlugField(_("Slug"), max_length=255)
    go_live_date = models.DateField(_("Go Live Date"))
    go_dead_date = models.DateField(_("Go Dead Date"), blank=True, null=True)

    # Relations
    league = models.ForeignKey("League")

    @staticmethod
    def current_seasons():
        return Season.objects.filter(go_live_date__lte=datetime.now()).filter(go_dead_date__gte=datetime.now())

    class Meta:
        ordering = ("name",)

    def __unicode__(self):
        return self.name


class Match(CommonModel):
    """ The match.
    """
    date = models.DateTimeField(_("Date"))
    team1_score = models.IntegerField(blank=True, null=True)
    team2_score = models.IntegerField(blank=True, null=True)

    # Relations
    season = models.ForeignKey("Season")
    division = models.ForeignKey("Division")
    team1 = models.ForeignKey("Team", related_name="team1")
    team2 = models.ForeignKey("Team", related_name="team2")

    class Meta:
        ordering = ("date",)
        verbose_name_plural = "Matches"

    def __unicode__(self):
        return "%s v %s" % (self.team1.abbr, self.team2.abbr)


class Team(CommonModel):
    """ The team model.
    """
    name = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(_("Slug"), max_length=255, unique=True)
    abbr = models.CharField(_("Abbr"), max_length=5)
    website = models.URLField(blank=True, null=True, verify_exists=False)
    address = models.CharField(_("Address"), max_length=255, blank=True)
    city = models.CharField(_("City"), max_length=255, blank=True)
    state = models.CharField(_("State"), max_length=2, blank=True)
    zip_code = models.CharField(_("Zip Code"), max_length=20, blank=True)
    description = models.TextField(_("Description"), blank=True)
    contact_name = models.CharField(_("Contact Name"), max_length=255, blank=True)
    contact_email = models.CharField(_("Contact Email"), max_length=255, blank=True)

    # Relations
    division = models.ForeignKey(Division)

    class Meta:
        ordering = ("name",)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('theleague_team', [str(self.slug)])


