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
    rating = models.IntegerField(default=1600)

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
        ordering = ('-rating',)

    def __unicode__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    """ This creates a user profile on invocation. """
    if created:
        Profile.objects.create(user=instance)
models.signals.post_save.connect(create_user_profile, sender=User)
