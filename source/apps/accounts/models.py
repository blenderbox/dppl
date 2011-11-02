from django.contrib.auth.models import User
from django.db import models

from apps.abstract.models import CommonModel


class Profile(CommonModel):
    """ This represents a user's profile. """
    user = models.OneToOneField(User, unique=True)
    avatar = models.ImageField(blank=True, null=True, upload_to="avatars")
    bio = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=1600)

    # Social
    twitter = models.CharField(blank=True, null=True, max_length=20)
    facebook = models.CharField(blank=True, null=True, max_length=50)
    linked_in = models.CharField(blank=True, null=True, max_length=50)
    website = models.URLField(blank=True, null=True, verify_exists=False)

    class Meta:
        ordering = ('-rating',)

    def __unicode__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    """ This creates a user profile on invocation. """
    if created:
        Profile.objects.create(user=instance)
models.signals.post_save.connect(create_user_profile, sender=User)
