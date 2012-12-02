import datetime

import dateutil
from django.db import models
from django.contrib.auth.models import User
from django.db.models import permalink, signals
from django.contrib.localflavor.us.models import PhoneNumberField

from savoy.core.constants import GENDER_CHOICES
from savoy.core.people.models import Person
from savoy.core.profiles.managers import *

class Profile(models.Model):
    user                  = models.OneToOneField(User, primary_key=True, related_name="profile")
    
    display_name          = models.CharField(blank=True, max_length=200)
    
    # Description
    one_line_description  = models.CharField(max_length=200, blank=True)
    bio                   = models.TextField(blank=True)
    
    #Location
    zip_code              = models.CharField(max_length=5, blank=True)
    display_on_map        = models.BooleanField(default=True)
    
    # Misc
    interests             = models.CharField(max_length=200, blank=True)
    occupation            = models.CharField(max_length=200, blank=True)
    gender                = models.CharField(max_length=32, choices=GENDER_CHOICES, blank=True)
    birth_date            = models.DateField(blank=True, null=True)
    signature             = models.TextField(blank=True)
    
    # Mobile
    mobile_number         = PhoneNumberField(blank=True)
    mobile_carrier        = models.ForeignKey('MobileCarrier', blank=True, null=True)
    
    # Avatar    
    avatar                = models.ImageField(upload_to='img/profiles/avatars/', blank=True)
    
    # Managers
    objects               = ProfileManager()
            
    def __unicode__(self):
      return self.user.username
    
    @property
    def age(self):
      TODAY = datetime.date.today()
      return '%s' % dateutil.relativedelta(TODAY, self.birth_date).years

    @property
    def name(self):
      if self.display_name:
        name = self.display_name
      else:
        name = self.user.username
      return name

    @property
    def full_name(self):
      return '%s' % self.user.get_full_name()

    @permalink
    def get_absolute_url(self):
      return ('profile_detail', None, { 'username': self.user.username })

    @permalink
    def get_edit_url(self):
      return ('edit_profile', None, { 'username': self.user.username })

    @property
    def sms_address(self):
      if (self.mobile and self.mobile_provider):
        return '%s@%s' % (re.sub('-', '', self.mobile), self.mobile_provider.domain)
        
    @property
    def person(self):
      try:
        return Person.objects.get(user=self.user)
      except:
        return None

signals.post_save.connect(Profile.objects.create_or_update, sender=User)
signals.post_delete.connect(Profile.objects.remove_orphans, sender=User)

class MobileCarrier(models.Model):
  """ MobileCarrier model """
  title             = models.CharField(max_length=25)
  domain            = models.CharField(max_length=50)

  def __str__(self):
    return '%s' % self.title



class ServiceType(models.Model):
  """ Service type model """
  title           = models.CharField(blank=True, max_length=100)
  url             = models.URLField(help_text='Be sure to use ending slash. (e.g. http://www.flickr.com/)')

  def __unicode__(self):
    return '%s' % self.title


class Service(models.Model):
  """ Service model """
  service         = models.ForeignKey(ServiceType)
  profile         = models.ForeignKey(Profile)
  username        = models.CharField(max_length=100)
  date_created    = models.DateTimeField()

  def __unicode__(self):
    return '%s' % self.username

  @property
  def url(self):
    return '%s%s' % (self.service.url, self.username)


class Website(models.Model):
  """ Website model """
  profile         = models.ForeignKey(Profile)
  title           = models.CharField(max_length=100)
  url             = models.URLField(verify_exists=True)

  def __str__(self):
    return '%s' % self.title