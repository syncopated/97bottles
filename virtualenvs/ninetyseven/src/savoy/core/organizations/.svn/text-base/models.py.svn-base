import datetime

from django.db import models
from django.contrib.auth.models import User
from tagging.fields import TagField
from tagging.models import Tag
from django.contrib.localflavor.us.models import PhoneNumberField

from savoy.core.geo.models import Place

class Organization(models.Model):
  """A person object is a description of an organization."""
  pre_name        = models.CharField(blank=True, max_length=200, help_text="Enter any prefix to the organization's name (The, An, A, etc.).")
  name            = models.CharField(max_length=200, help_text="Enter the organization's name.")
  slug            = models.SlugField(help_text="A slug is a URL-friendly version of the organization's name. It is auto-populated.")
  industry        = models.ForeignKey('Industry', blank=True, null=True, related_name="organizations")
  description     = models.TextField(blank=True, help_text="Enter this organization's description.")
  locations       = models.ManyToManyField(Place, blank=True, null=True, related_name="organizations")
  phone1          = PhoneNumberField(blank=True, help_text='Enter the phone number for this organization.')
  phone2          = PhoneNumberField(blank=True, help_text='Enter a second phone number for this organization.')
  fax             = PhoneNumberField(blank=True, help_text='Enter the fax number for this organization.')
  email           = models.EmailField(blank=True, help_text='Enter the e-mail address for this organization.')
  url             = models.URLField(blank=True,verify_exists=True, help_text='Enter the website URL for this organization.')
  tags            = TagField(help_text="Add tags for this person.")
  date_created    = models.DateTimeField(default=datetime.datetime.now, editable=False)

  def __unicode__(self):
    return self.full_name()
  
  def full_name(self):
    """ Returns the full name of the organization, prepending the pre_name to the name. """
    return " ".join(b for b in (self.pre_name, self.name) if b)
  
  def get_absolute_url(self):
    """ Returns the URL to this organization's detail page. """
    return "/organizations/%s/" % (self.slug)
  
  def get_people(self):
    """Returns all people who have a role in this organization."""
    from savoy.core.people.models import Role
    roles = Role.objects.filter(organization=self)
    people = []
    for role in roles:
      person = role.person
      person.role = role
      if not person in people:
        people.append(person)
    return people
    
  class Meta:
    ordering = ['name']
    
class Industry(models.Model):
  name = models.CharField(blank=True, max_length=200)
  slug = models.SlugField()
  
  def __unicode__(self):
    return self.name
  
  class Meta:
    verbose_name_plural = "Industries"