import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals, permalink
from tagging.fields import TagField
from tagging.models import Tag
from django.contrib.localflavor.us.models import PhoneNumberField

from savoy.core.organizations.models import Organization
from savoy.core.geo.models import Place
from savoy.core.people.managers import *


class Person(models.Model):
  """A person object is a description of an individual person."""
  salutation      = models.CharField(blank=True, max_length=200, help_text="Enter any prefix to the person's name (initials, Dr., Mr., Mrs., etc.).")
  first_name      = models.CharField(max_length=200, help_text="Enter the person's first name.")
  middle_name     = models.CharField(max_length=200, blank=True, help_text="Enter the person's middle name.")
  last_name       = models.CharField(max_length=200, blank=True, help_text="Enter the person's last name.")
  suffix          = models.CharField(blank=True, max_length=100, help_text="Enter any suffix to the person's name (Jr., CPA, III, etc.)")
  slug            = models.SlugField(help_text="A slug is a URL-friendly version of the person's name. It is auto-populated.")
  user            = models.ForeignKey(User, blank=True, null=True, help_text="If this person is a user of this site, select their username.", related_name="person")
  bio             = models.TextField(blank=True, help_text="Enter this person's bio.")
  home            = models.ForeignKey(Place, blank=True, null=True, help_text="Select or add this person's home address.", related_name="home")
  work            = models.ForeignKey(Place, blank=True, null=True, help_text="Select or add this person's work address.", related_name="work")
  home_phone      = PhoneNumberField(blank=True, null=True, help_text='Enter the home phone number for this person.')
  work_phone      = PhoneNumberField(blank=True, null=True, help_text='Enter the work phone number for this person.')
  mobile_phone    = PhoneNumberField(blank=True, null=True, help_text='Enter the mobile phone number for this person.')
  fax             = PhoneNumberField(blank=True, null=True, help_text='Enter the fax number for this person.')
  home_email      = models.EmailField(blank=True, null=True, help_text='Enter the home e-mail address for this person.')
  work_email      = models.EmailField(blank=True, null=True, help_text='Enter the work e-mail address for this person.')
  personal_url    = models.URLField(blank=True, null=True, verify_exists=True, help_text='Enter the personal website URL for this person.')
  professional_url= models.URLField(blank=True, null=True, verify_exists=True, help_text='Enter the website URL for this person\'s company or organization.')
  photo           = models.ImageField(upload_to="img/person_photos/", blank=True, null=True, height_field='photo_height', width_field='photo_width',help_text="Upload a photo of this person.")
  photo_width     = models.IntegerField(blank=True, null=True, editable=False)
  photo_height    = models.IntegerField(blank=True, null=True, editable=False)
  tags            = TagField(help_text="Add tags for this person.")
  date_created    = models.DateTimeField(default=datetime.datetime.now, editable=False)
  
  objects = PersonManager()
  
  def __unicode__(self):
    return self.first_name + " " + self.last_name
  
  def name(self):
    """ Returns the name of the person, in FirstName LastName format. """
    if self.first_name or self.last_name:
      return " ".join(b for b in (self.first_name, self.last_name) if b)
    else:
      return self.user.username

  def full_name(self):
    """ Returns the full name of the person, appending salutation, first name, last name, and suffix. """
    return " ".join(b for b in (self.salutation, self.first_name, self.middle_name, self.last_name, self.suffix) if b)

  def full_name_last_first(self):
    """ Returns the full name of the person, appending salutation, first name, last name, and suffix, in sort order (last first). """
    return ", ".join(b for b in (self.last_name, self.salutation, self.first_name, self.middle_name, self.suffix) if b)
  
  def get_organizations(self):
    """Returns all the organizations this person has a role at."""
    from savoy.core.people.models import Role
    organizations = Role.objects.filter(person=self)
    person_orgs = []
    for role in organizations:
      if role.organization not in person_orgs:
        person_orgs.append(role.organization)
    return person_orgs
  
  def get_portfolio_disciplines(self):
    """Returns all the portfolio.discipline object this person has performed."""
    from savoy.contrib.portfolio.models import Role
    disciplines = self.project_role.all()
    return [ role.discipline for role in disciplines if role.discipline not in disciplines ]

  def organizations(self):
    """Returns a string of organizations for use in the admin list display."""
    return ", ".join([ unicode(role.organization) for role in Role.objects.filter(person=self) ])
  
  @permalink
  def get_absolute_url(self):
    """ Returns the URL for the detail page of this person, unless the person is a user, in which case it returns the detail page for the user. """
    if self.user:
      return ('savoy.core.profiles.profile_detail', None, { 'username': self.user.username })
    else:
      return ('savoy.core.people.person_detail', None, { 'slug': self.slug })
  
  def get_person_url(self):
    """ Returns the URL for the detail page of this person. """
    return "/people/%s/" % (self.slug)

  class Meta:
    verbose_name_plural = "People"
    get_latest_by = 'date_created'
    ordering = ("last_name", "first_name")

signals.post_save.connect(Person.objects.create_or_update, sender=User)

class Role(models.Model):
  """An office is a position held by a person at an organization."""
  person        = models.ForeignKey(Person, help_text="Select or add a person who holds a role at an organization.")
  organization  = models.ForeignKey(Organization, blank=True, null=True)
  role          = models.CharField(max_length=200, help_text="Enter the role or job title this person holds or held.")
  start_date    = models.DateField(blank=True, null=True, help_text="Enter the date the person took over the role.")
  end_date      = models.DateField(blank=True, null=True, help_text="Enter the date the person left the role. Leave this blank if this person is currently holds the role.")

  def __unicode__(self):
    return self.role
  
  def display_role(self):
    """ Returns the role for display. """
    if self.role != ' ':
      display_role = self.role
    else:
      display_role = None
    return display_role

class BioHighlight(models.Model):
  """A bio highlight is short description of an event or achievement in a Persons career."""
  person        = models.ForeignKey(Person, help_text="Select or add a person who holds a role at an organization.")
  highlight     = models.CharField(max_length=255, help_text="Enter the text of the highlight.")

  def __unicode__(self):
    return self.person.__unicode__() + ", " + self.highlight