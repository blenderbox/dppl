from django.contrib.auth.models import User
from django.db import models

from imagekit.models import ImageSpec
from imagekit.processors.resize import SmartResize

from apps.abstract.models import CommonModel
from apps.theleague.models import Team
from app_utils.image_processors import Pixelate


class Profile(CommonModel):
    """ This represents a user's profile. """
    user = models.OneToOneField(User, unique=True)
    slug = models.SlugField("Slug", max_length=255)
    bio = models.TextField(blank=True, null=True)

    # TrueSkill Rating
    # To sort players by rating, sort by their exposure. For instance, best to
    # worst would be Profile.object.order_by('-exposure')
    # To figure out what this player's rank is in the league, something like
    # this should work:
    # Profile.objects.filter(exposure__gte=self.exposure).order_by(
    #   '-exposure').count()
    # Exposures which are <= 0 should appear as "unranked" to the user.
    mu = models.FloatField(blank=True, null=True)
    sigma = models.FloatField(blank=True, null=True)
    exposure = models.FloatField(default=0)

    # Avatarz
    THUMB_SIZE = (46, 46)
    AVATAR_FORMAT = "JPEG"
    DEFAULT_AVATAR = "avatars/default.jpg"
    avatar = models.ImageField(default=DEFAULT_AVATAR, upload_to="avatars")
    pixelate_avatar = ImageSpec(
            [Pixelate(), SmartResize(*THUMB_SIZE)],
            image_field='avatar',
            format=AVATAR_FORMAT,
            )
    thumbnail_avatar = ImageSpec(
            [SmartResize(*THUMB_SIZE)],
            image_field='avatar',
            format=AVATAR_FORMAT,
            )

    # Social
    twitter = models.CharField(blank=True, null=True, max_length=20)
    facebook = models.CharField(blank=True, null=True, max_length=50)
    linked_in = models.CharField(blank=True, null=True, max_length=50)
    website = models.URLField(blank=True, null=True, verify_exists=False)

    team = models.ForeignKey(Team, related_name="profile_team")

    class Meta:
        ordering = ('-exposure',)

    def __unicode__(self):
        return self.user.username

    @models.permalink
    def get_absolute_url(self):
        return ('theleague_team_member', [str(self.team.slug), str(self.slug)])

    @property
    def full_name(self):
        if self.user.first_name == "":
            return self.user.username
        return ("%s %s" % (self.user.first_name, self.user.last_name)).strip()


def create_user_profile(sender, instance, created, **kwargs):
    """ This creates a user profile on invocation. """
    if created:
        Profile.objects.create(user=instance)
models.signals.post_save.connect(create_user_profile, sender=User)
