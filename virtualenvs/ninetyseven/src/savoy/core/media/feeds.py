import datetime
import time

from django.conf import settings
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType

from savoy.core.media.models import *

site = Site.objects.get(id=settings.SITE_ID)
site_url = "http://%s/" % site.domain



class LatestPhotos(Feed):
  """ A feed of the latest photos. """
  
  title_template = 'media/photos/feeds/photo_title.html'
  description_template = 'media/photos/feeds/photo_description.html'
  
  title = "%s: Latest photos" % site.name
  link = site_url
  description = "The latest photos at %s" % site.name

  def items(self):
    return Photo.objects.filter(flickrphoto__owner__nsid=settings.FLICKR_USERID).order_by('-date_published')[:15]

  def item_pubdate(self, item):
      return item.date_published

  item_author_name  = ""
  item_author_email = ""
  item_author_link  = ""



class LatestFavoritePhotos(Feed):
  """ A feed of the latest photo favorites. """
  
  title_template = 'media/photos/feeds/photo_title.html'
  description_template = 'media/photos/feeds/photo_description.html'
  
  title = "%s: Latest photo favorites" % site.name
  link = site_url
  description = "The latest photo favorites at %s" % site.name

  def items(self):
    return Photo.objects.exclude(flickrphoto__owner__nsid=settings.FLICKR_USERID).order_by('-date_published')[:15]

  def item_pubdate(self, item):
      return item.date_published

  item_author_name  = ""
  item_author_email = ""
  item_author_link  = ""  