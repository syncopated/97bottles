import datetime
from tagging.fields import TagField

from django.db import models
from django.db.models import permalink

from savoy.contrib.bookmarks.managers import *

class Bookmark(models.Model):
  url             = models.URLField(help_text="Enter the URL to the bookmarked page.", max_length=400)
  screenshot      = models.URLField(help_text="Enter the URL to a screenshot of the bookmarked page.", max_length=400, blank=True, null=True)
  title           = models.CharField(max_length=250, help_text="Enter the title of the bookmarked page.")
  slug            = models.SlugField(max_length=250)
  rating          = models.PositiveSmallIntegerField(blank=True, null=True, help_text="Enter the rating of the bookmarked page.")
  description     = models.TextField(blank=True, help_text="Enter a brief description of the bookmarked page.")
  tags            = TagField(help_text="Enter tags for the bookmarked page.")
  date_published  = models.DateTimeField(default=datetime.datetime.now, help_text="Enter the date this bookmark should be published.")
  date_updated    = models.DateTimeField(blank=True, null=True, editable=False)
  private         = models.BooleanField(default=False)

  # Managers
  objects         = models.Manager()
  live_bookmarks  = LiveBookmarkManager()
  
  def __unicode__(self):
    return self.title

  @permalink
  def get_absolute_url(self):
    """ Returns the URL to the detail page for this bookmark. """
    y = self.date_published.strftime("%Y").lower()
    m = self.date_published.strftime("%b").lower()
    d = self.date_published.strftime("%d").lower()
    s = str(self.slug)
    return ('bookmark_detail', None, {'year': y, 'month': m, 'day': d, 'slug': s})

  def url_string(self):
    """ Returns a string representation of the URL, useful for constructing comment feed URLs. """
    y = self.date_published.strftime("%Y").lower()
    m = self.date_published.strftime("%b").lower()
    d = self.date_published.strftime("%d").lower()
    s = str(self.slug)
    return "%s/%s/%s/%s/" % (y,m,d,s)

  def magnolia_bookmark(self):
    """ If this bookmark is from ma.gnolia, returns the related MagnoliaBookmark object. """
    try:
      return MagnoliaBookmark.objects.get(bookmark=self)
    except:
      return None
  
  def delicious_bookmark(self):
    """ If this bookmark is from del.icio.us, returns the related DeliciousBookmark object. """
    try:
      return DeliciousBookmark.objects.get(bookmark=self)
    except:
      return None

  def source(self):
    """ Returns a string representation of the source of this bookmark (i.e. 'magnoila', 'delicious', or 'local'). """
    if self.magnolia_bookmark():
      return "ma.gnolia"
    elif self.delicious_bookmark():
      return "del.icio.us"
    else:
      return "local"

  def description_with_link(self, link_string=None):
    """ Returns the description field with an appended link to the url. Default link text is 'Visit site &raquo;'. """
    if not link_string:
      link_string = "Visit site &raquo;"
    link = ' <a href="%s" title="%s">%s</a>' % (self.url, self.title, link_string)
    return self.description + link
  
  def save(self, force_insert=False, force_update=False):
    """ Stores the date updated, and then saves the bookmark. """
    self.date_updated = datetime.datetime.now()
    super(Bookmark, self).save(force_insert=force_insert, force_update=force_update)
  
  class Meta:
    ordering = ['-date_published']
     
      
class DeliciousBookmark(models.Model):
  bookmark = models.ForeignKey(Bookmark)
  hash = models.CharField(blank=True, max_length=250)

  def __unicode__(self):
    return self.bookmark.title


class MagnoliaBookmark(models.Model):
  bookmark = models.ForeignKey(Bookmark)
  magnolia_id = models.CharField(max_length=250)
  owner = models.CharField(max_length=200)

  def __unicode__(self):
    return self.bookmark.title