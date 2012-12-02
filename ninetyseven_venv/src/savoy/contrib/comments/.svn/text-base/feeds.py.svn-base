import datetime
import time

from django.conf import settings
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType

from savoy.contrib.comments.models import Comment

site = Site.objects.get(id=settings.SITE_ID)
site_url = "http://%s/" % site.domain

class LatestComments(Feed):
  """ A feed of the latest comments. """
  
  title_template = 'comments/feeds/comment_title.html'
  description_template = 'comments/feeds/comment_description.html'
  
  title = "%s: Latest comments" % site.name
  link = site_url
  description = "The latest comments at %s" % site.name

  def items(self):
    return Comment.approved_comments.all().order_by('-date_submitted')[:35]

  def item_pubdate(self, item):
    return item.date_submitted

  def item_author_name(self, item):
    try:
      return item.author_name.encode("utf-8")
    except:
      return 'Unknown'
      
  def item_link(self, item):
    # This is not quite ideal, because it doesn't add "#cXXXX" to the comment URL.
    try:
      return item.parent_object().get_absolute_url()
    except:
      return site_url

  def item_author_email(self, item):
    return ""

  def item_author_link(self, item):
    return item.author_url.encode("utf-8")