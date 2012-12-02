import datetime

from django.db import models
from django.db.models import permalink
from django.db.models import signals
from django.contrib.markup.templatetags.markup import *
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from tagging.fields import TagField
from typogrify.templatetags.typogrify import typogrify

from savoy.core.constants import BLOG_STATUS_CHOICES, BLOG_ENTRY_STATUS_CHOICES, MARKUP_CHOICES
from savoy.core.people.models import Person
from savoy.core.geo.models import Place, GeolocatedItem
from savoy.contrib.blogs.managers import *


class Blog(models.Model):
  """
  A blog is a collection of entries, authored by one or more users.
  """
  authors         = models.ManyToManyField(Person)
  title           = models.CharField(max_length=250)
  slug            = models.SlugField(unique=True)
  date_created    = models.DateTimeField(default=datetime.datetime.now)
  status          = models.IntegerField('Blog status', choices=BLOG_STATUS_CHOICES, default=1)
  featured        = models.BooleanField('Featured', default=False)
  tags            = TagField(help_text="Add tags for this entry (space separated).")
  objects         = models.Manager()
  active_blogs    = ActiveBlogManager()
  featured_blogs  = FeaturedBlogManager()
  
  def __unicode__(self):
    return self.title
  
  @permalink
  def get_absolute_url(self):
    """ Returns the URL to the detail page for this blog. """
    return ('blog_index', (), { 'blog_slug': self.slug })
  
  class Meta:
    ordering = ['title', 'date_created']
    get_latest_by = 'date_created'
    
    
class Entry(models.Model):
  """
  An entry is a post within a blog.
  """
  blogs                   = models.ManyToManyField(Blog, help_text='Select the blogs this entry belongs to.', default="1")
  author                  = models.ForeignKey(Person, help_text='Select the author of this entry.')
  posted_from             = models.ForeignKey(Place, help_text='Select the place from which this entry was posted.', blank=True, null=True)
  title                   = models.CharField('Entry title', max_length=250, help_text='Enter the title of this blog entry.')
  slug                    = models.SlugField('Slug', help_text='The slug is a URL-friendly version of the title. It is auto-populated.', unique_for_date="date_published")
  intro                   = models.TextField('Entry intro', help_text='Enter the intro to this blog entry, usually one or two paragraphs.', blank=True)
  body                    = models.TextField('Entry body', help_text='Enter the main content of this blog entry.')
  body_extended           = models.TextField('Entry body cont', help_text='Enter the secondary content of this blog entry.', blank=True)
  summary                 = models.TextField('Entry summary', help_text='Enter a brief summary of this blog entry.', blank=True)
  date_published          = models.DateTimeField(help_text="Select the date and time this entry was posted.", default=datetime.datetime.now)
  date_created            = models.DateTimeField(editable=False, default=datetime.datetime.now)
  date_updated            = models.DateTimeField(editable=False)
  tags                    = TagField(help_text="Add tags for this entry (space separated).")
  status                  = models.IntegerField('Entry status', help_text="Select the status of this blog entry.", choices=BLOG_ENTRY_STATUS_CHOICES, default=2)
  enable_comments         = models.BooleanField('Enable comments', help_text="Select 'True' if you wish to enable visitors to comment on this entry.", default=True)
  markup_language         = models.CharField(max_length=100, default="markdown", choices=MARKUP_CHOICES, help_text="Select the markup language you would like to process this content with.")
  process_inlines         = models.BooleanField('Process inline objects for this entry', help_text="Select 'True' if you wish to display this entry with inline objects parsed and applied.", default=True)
  featured                = models.BooleanField('Featured', default=False, help_text="Select 'True' if if this is currently a featured blog entry.")
  objects                 = models.Manager()
  live_entries            = LiveEntryManager()
  featured_entries        = FeaturedEntryManager()
  
  def __unicode__(self):
      return self.title

  @permalink
  def get_absolute_url(self):
    """ Returns the URL to the detail page for this blog entry. """
    y = self.date_published.strftime("%Y").lower()
    m = self.date_published.strftime("%b").lower()
    d = self.date_published.strftime("%d").lower()
    s = str(self.slug)
    if settings.USE_SINGLE_BLOG_URLS:
      return ('savoy.contrib.blogs.views.blog_entry_detail', None, { 'year': y, 'month': m, 'day': d, 'slug': s })
    else:
      return ('savoy.contrib.blogs.views.blog_entry_detail', None, { 'blog_slug': str(self.blogs.all()[0].slug), 'year': y, 'month': m, 'day': d, 'slug': s })

  def url_string(self):
    """ Returns a string representation of the URL, useful for constructing comment feed URLs. """
    b = self.blogs.all()[0].slug
    y = self.date_published.strftime("%Y").lower()
    m = self.date_published.strftime("%b").lower()
    d = self.date_published.strftime("%d").lower()
    s = str(self.slug)
    if settings.USE_SINGLE_BLOG_URLS:
      return "%s/%s/%s/%s/" % (y,m,d,s)
    else:
      return "%s/%s/%s/%s/%s/" % (b,y,m,d,s)  

  def _render_markup(self, value):
    """ Picks the right markup filter, applies it, applies typogrify, and also processes inlines, if necessary."""
    from django.contrib.markup.templatetags.markup import markdown, textile, restructuredtext
    import markdown
    from typogrify.templatetags.typogrify import typogrify
    from savoy.contrib.inlines.templatetags.inlines import inlines
    
    if self.markup_language:
      if self.markup_language == 'markdown':
        value = markdown.markdown(value, safe_mode=False)
      elif self.markup_language == 'textile':
        value = textile(value)
      elif self.markup_language == 'restructured_text':
        value = restructured_text(value)
    
    value = typogrify(value)
    
    if self.process_inlines:
      value = inlines(value)
    return value
  
  def intro_rendered_markup(self):
    """ The intro field, with any markup filters, typogrify, and inlines applied. """
    return self._render_markup(self.intro)
  
  def body_rendered_markup(self):
    """ The body field, with any markup filters, typogrify, and inlines applied. """
    return self._render_markup(self.body)
  
  def body_extended_rendered_markup(self):
    """ The body_extended field, with any markup filters, typogrify, and inlines applied. """
    return self._render_markup(self.body_extended)
  
  def summary_rendered_markup(self):
    """ The summary field, with any markup filters, typogrify, and inlines applied. """
    return self._render_markup(self.summary)

  def save(self, force_insert=False, force_update=False):
    """
    Processes text, creates any related items, and then saves the entry.
    """
    self.date_updated = datetime.datetime.now()
    super(Entry, self).save(force_insert=force_insert, force_update=force_update) # Call the "real" save() method
    if self.posted_from != None:
      GeolocatedItem.objects.create_or_update(self, address=self.posted_from.geolocation_address())

  class Meta:
    verbose_name_plural = 'Entries'
    get_latest_by = 'date_published'
    ordering = ['-date_published']
    
    
signals.post_delete.connect(GeolocatedItem.objects.remove_orphans, sender=Entry)