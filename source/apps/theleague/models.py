from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.abstract.models import CommonModel



class Division(CommonModel):
    """
    """
    name = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(_("Slug"), max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class League(CommonModel):
    """
    """
    name = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(_("Slug"), max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Match(CommonModel):
    """
    """
    date = models.DateTimeField(_("Date"))

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Season(CommonModel):
    """
    """
    name = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(_("Slug"), max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Team(CommonModel):
    """
    """
    name = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(_("Slug"), max_length=255, unique=True)
    address = models.CharField(_("Address"), max_length=255, blank=True)
    city = models.CharField(_("City"), max_length=255, blank=True)
    state = models.CharField(_("State"), max_length=2, blank=True)
    zip_code = models.CharField(_("Zip Code"), max_length=20, blank=True)
    description = models.TextField((_("Description"), blank=True)
    contact_name = models.CharField(_("Contact Name"), max_length=255, blank=True)
    contact_email = models.CharField(_("Contact Email"), max_length=255, blank=True)

    # Relations
    division = models.ForeignKey(Division)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name