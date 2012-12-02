import datetime
import time

from django.conf import settings
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType

from savoy.contrib.podcasts.models import *

site = Site.objects.get(id=settings.SITE_ID)
site_url = "http://%s/" % site.domain



class LatestEpisodes(Feed):
  title = "%s: Latest podcast episodes" % site.name
  link = site_url
  description = "The latest podcast episodes at %s" % site.name

  title_template = 'podcasts/feeds/episode_title.html'
  description_template = 'podcasts/feeds/episode_description.html'

  def items(self):
    return Episode.objects.all().order_by('-date_published')[:15]

  def item_pubdate(self, item):
      return item.date_published

  item_author_name = ""
  item_author_email = ""
  item_author_link = ""
  item_enclosure_length = 32000
  item_enclosure_mime_type = "audio/mpeg"
  def item_enclosure_url(self, item):
    return item.audio_files.all()[0].audio.audio_file_url
    
    
class LatestEpisodesPerShow(Feed):
  def get_object(self, bits):
    if len(bits) != 1:
      raise ObjectDoesNotExist
    return Show.objects.get(slug=bits[0])
    
  def title(self, obj):
    return "%s: %s" % (site.name, obj.name)
      
  link = site_url
  
  def description(self, obj):
    description = "The latest %s episodes at %s" % (obj.name, site.name)

  title_template = 'podcasts/feeds/latest-episodes_title.html'
  description_template = 'podcasts/feeds/latest-episodes_description.html'

  def items(self, obj):
    return Episode.objects.all().filter(show=obj).order_by('-date_published')[:15]

  def item_pubdate(self, item):
      return item.date_published

  item_author_name = ""
  item_author_email = ""
  item_author_link = ""
  item_enclosure_length = 32000
  item_enclosure_mime_type = "audio/mpeg"
  def item_enclosure_url(self, item):
    return item.audio_files.all()[0].audio.audio_file_url