import datetime
from dateutil import relativedelta
import re

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField

from savoy.core.geo.models import City, GeolocatedItem
from savoy.core.new.profiles.managers import *

class Profile(models.Model):
    """ Profile model """
    GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Other'),
    )
    user                  = models.OneToOneField(User, primary_key=True, related_name="profile")
    display_name          = models.CharField(_('display name'), blank=True, max_length=200)
    one_line_description  = models.CharField(max_length=200, blank=True)
    bio                   = models.TextField(blank=True)
    gender                = models.PositiveSmallIntegerField(_('gender'), choices=GENDER_CHOICES, blank=True, null=True)
    avatar                = models.FileField(_('avatar'), upload_to='img/profiles/avatars/', blank=True, null=True)
    birth_date            = models.DateField(_('birth date'), blank=True, null=True)
    city                  = models.ForeignKey(City, blank=True, null=True)
    mobile_number         = PhoneNumberField(_('mobile'), blank=True, null=True)
    mobile_provider       = models.ForeignKey('MobileProvider', blank=True, null=True)
    
    objects               = ProfileManager()
  
    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')

    def __unicode__(self):
        return u"%s" % self.name
    
    @property
    def name(self):
      if self.display_name:
        return self.display_name
      else:
        return self.user.username
    
    @property
    def age(self):
        TODAY = datetime.date.today()
        if self.birth_date:
            return u"%s" % relativedelta.relativedelta(TODAY, self.birth_date).years
        else:
            return None

    @property
    def person(self):
      try:
        return Person.objects.get(user=self.user)
      except Person.DoesNotExist:
        return None
                
    @permalink
    def get_absolute_url(self):
      return ('profile_detail', None, { 'username': self.user.username })

    @property
    def sms_address(self):
      if (self.mobile and self.mobile_provider):
          return u"%s@%s" % (re.sub('-', '', self.mobile), self.mobile_provider.domain)
      
    def save(self, force_insert=False, force_update=False):
      super(Profile, self).save(force_insert=force_insert, force_update=force_update)
      if self.city and self.city.location():
        GeolocatedItem.objects.create_or_update(self, location=(self.city.location().latitude, self.city.location().longitude), city=self.city)
            
signals.post_save.connect(Profile.objects.create_or_update, sender=User)
signals.post_delete.connect(Profile.objects.remove_orphans, sender=User)

class MobileProvider(models.Model):
    """ MobileProvider model """
    title             = models.CharField(_('title'), max_length=25)
    domain            = models.CharField(_('domain'), max_length=50, unique=True)

    class Meta:
        verbose_name = _('mobile provider')
        verbose_name_plural = _('mobile providers')

    def __unicode__(self):
        return u"%s" % self.title


class ServiceType(models.Model):
    """ Service type model """
    title           = models.CharField(_('title'), blank=True, max_length=100)
    url             = models.URLField(_('url'), blank=True, help_text='URL with a single \'{user}\' placeholder to turn a username into a service URL.', verify_exists=False)

    class Meta:
        verbose_name = _('service type')
        verbose_name_plural = _('service types')

    def __unicode__(self):
        return u"%s" % self.title


class Service(models.Model):
    """ Service model """
    service         = models.ForeignKey(ServiceType)
    profile         = models.ForeignKey(Profile, related_name="services")
    username        = models.CharField(_('Username'), max_length=100,)
    created         = models.DateTimeField(auto_now_add=True)
    modified        = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('service')
        verbose_name_plural = _('services')
    
    def __unicode__(self):
        return u"%s" % self.username
    
    @property
    def service_url(self):
        return re.sub('{user}', self.username, self.service.url)
    
    @property
    def title(self):
        return u"%s" % self.service.title


class Link(models.Model):
    """ Service type model """
    profile         = models.ForeignKey(Profile, related_name="links")
    title           = models.CharField(_('title'), max_length=100)
    url             = models.URLField(_('url'), verify_exists=True)

    class Meta:
        verbose_name = _('link')
        verbose_name_plural = _('links')

    def __unicode__(self):
        return u"%s" % self.title