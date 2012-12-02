import datetime

from django.db import models
from django.utils.encoding import smart_unicode
from django.db.models import permalink
from django.utils.encoding import force_unicode

from savoy.core.organizations.models import Organization
from savoy.core.people.models import Person

# Create your models here.

class Medium(models.Model):
    name  = models.CharField(max_length=250)
    slug  = models.SlugField()
    
    def __unicode__(self):
      return self.name

    class Meta:
      ordering = ['name']

class Discipline(models.Model):
    name  = models.CharField(max_length=250)
    slug  = models.SlugField()
    
    def __unicode__(self):
      return self.name
        
    class Meta:
      ordering = ['name']

class Project(models.Model):
  title           = models.CharField(max_length=250)
  slug            = models.SlugField()
  url             = models.URLField('Project URL', blank=True)
  summary         = models.TextField(blank=True)
  description     = models.TextField(blank=True)
  client          = models.ForeignKey(Organization)
  mediums         = models.ManyToManyField(Medium)
  disciplines     = models.ManyToManyField(Discipline)
  date_published  = models.DateTimeField(default=datetime.datetime.now)
  date_completed  = models.DateField()
  in_development  = models.BooleanField()
  is_public       = models.BooleanField(default=True)

  def __unicode__(self):
    return self.title

  @permalink
  def get_absolute_url(self):
    """ Returns the URL to this project's detail page. """
    y = self.date_published.strftime("%Y").lower()
    m = self.date_published.strftime("%b").lower()
    d = self.date_published.strftime("%d").lower()
    s = str(self.slug)
    return ('project_detail', None, {'year': y, 'month': m, 'day': d, 'slug': s})

  class Meta:
    ordering = ['-date_completed']
      
class Role(models.Model):
  """A Role is a relationship between a person and a portfolio Project."""
  project       = models.ForeignKey(Project, help_text="Add or select the project this image is associated with.")
  person        = models.ForeignKey(Person, help_text="Add or select the person.", related_name="project_role")
  discipline    = models.ForeignKey(Discipline, help_text="Add or select the discipline this person performed.", related_name="project_discipline")

  def __unicode__(self):
    return force_unicode(self.project) + ": " + force_unicode(self.person) + ", " + force_unicode(self.discipline)
         
class Image(models.Model):
  """An Image is an image attached to a portfolio Project."""
  project             = models.ForeignKey(Project, help_text="Add or select the portfolio this image is associated with.")
  
  # Basic
  title               = models.CharField(max_length=250, help_text="Enter the title of this photo.")
  slug                = models.SlugField(max_length=200, help_text='The slug is a URL-friendly version of the title. It is auto-populated.')
  description         = models.TextField(blank=True, help_text='Add a caption for the photo.')

  # The image
  image               = models.ImageField(upload_to='portfolio_images/%Y/%m/%d', width_field='image_width', height_field='image_height', blank=True, help_text='Should be JPEG format. Larger pixel sizes are better.')
  image_width         = models.IntegerField(blank=True, null=True, editable=False)
  image_height        = models.IntegerField(blank=True, null=True, editable=False)
    
  # Dates
  date_created        = models.DateTimeField()
    
  def __unicode__(self):
    return force_unicode(self.project) + ': ' + force_unicode(self.title)
    
    
class Testimonial(models.Model):
  body          = models.TextField(blank=True)
  person        = models.ForeignKey(Person, help_text="Add or select the person.")
  project       = models.ForeignKey(Project, help_text="Add or select the project this image is associated with.", blank=True, null=True)
  featured      = models.BooleanField(default=False)
  
  def __unicode__(self):
    return force_unicode(self.person) + ", " + force_unicode(self.body)

  class Admin:
     pass