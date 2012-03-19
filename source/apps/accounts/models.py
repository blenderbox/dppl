import random
import string

from django.contrib.auth.models import User
from django.db import models

from imagekit.models import ImageSpec
from imagekit.processors import resize

from apps.abstract.models import CommonModel
from apps.theleague.models import Team
from app_utils.image_processors import Pixelate


def get_path(instance, filename):
    """ Normalizes the filename. """
    chars = string.ascii_lowercase + string.digits
    return "avatars/%s%s.%s" % (
                instance.pk,
                ''.join(random.choice(chars) for x in range(5)),
                filename.rsplit('.', 1)[1]
                )


class Profile(CommonModel):
    """ This represents a user's profile.

    To sort players by rating, sort by their exposure. For instance, best to
    worst would be:
        Profile.object.order_by('-exposure')

    To figure out what this player's rank is in the league, something like
    this should work:
        Profile.objects.filter(exposure__gte=self.exposure).order_by(
            '-exposure').count()

    Exposures which are <= 0 should appear as "unranked" to the user.
    """
    user = models.OneToOneField(User, unique=True)
    slug = models.SlugField("Slug", max_length=255)
    bio = models.TextField(blank=True, null=True)
    include_in_team = models.BooleanField(default=True)

    # TrueSkill Rating
    mu = models.FloatField(blank=True, null=True)
    sigma = models.FloatField(blank=True, null=True)
    exposure = models.FloatField(default=0)

    # Avatarz
    THUMB_SIZE = (46, 46)
    AVATAR_FORMAT = "JPEG"
    avatar = models.ImageField(upload_to=get_path, blank=True, null=True)
    pixelate_avatar = ImageSpec(
            [Pixelate(), resize.SmartCrop(*THUMB_SIZE)],
            image_field='avatar',
            format=AVATAR_FORMAT,
            )
    thumbnail_avatar = ImageSpec(
            [resize.SmartCrop(*THUMB_SIZE)],
            image_field='avatar',
            format=AVATAR_FORMAT,
            )

    # Social
    twitter = models.CharField("Twitter handle", blank=True, null=True,
            max_length=20)
    facebook = models.CharField("Facebook username", blank=True, null=True,
            max_length=50)
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

    def ranking(self):
        """ Where this player ranks compared to the other players. """
        if self.exposure <= 0:
            return "Unranked"
        else:
            return Profile.objects.filter(
                    exposure__gte=self.exposure).order_by('-exposure').count()

    def rating(self):
        if self.exposure <= 0:
            return "Unrated"
        else:
            return self.exposure

    @property
    def full_name(self):
        if self.user.first_name == "":
            return self.user.username
        return ("%s %s" % (self.user.first_name, self.user.last_name)).strip()

    @property
    def facebook_url(self):
        if self.facebook:
            return "http://facebook.com/%s" % self.facebook.strip()
        else:
            return ""

    @property
    def twitter_url(self):
        if self.twitter:
            return "http://twitter.com/%s" % self.twitter.strip()
        else:
            return ""

    @property
    def linked_in_url(self):
        if self.linked_in:
            return "http://www.linkedin.com/in/%s" % self.linked_in.strip()
        else:
            return ""


def delete_user_profile(sender, instance, **kwargs):
    """ This deletes the user profile when the User is deleted. """
    try:
        Profile.objects.get(user=instance).delete()
    except Profile.DoesNotExist:
        pass
models.signals.post_delete.connect(delete_user_profile, sender=User)
