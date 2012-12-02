import datetime
import time

from django.conf import settings
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType

from savoy.contrib.statuses.models import Status

site = Site.objects.get(id=settings.SITE_ID)
site_url = "http://%s/" % site.domain

class LatestStatuses(Feed):
  """ A feed of the latest statuses. """
  
  title_template = 'statuses/feeds/status_title.html'
  description_template = 'statuses/feeds/status_description.html'
  
  title = "%s: Latest statuses" % site.name
  link = site_url
  description = "The latest statuses at %s" % site.name

  def items(self):
    return Status.objects.all().order_by('-date_published')[:15]

  def item_pubdate(self, item):
      return item.date_published

  item_author_name = ""
  item_author_email = ""
  item_author_link = ""