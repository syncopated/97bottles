import datetime
import time

from django.conf import settings
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import *

from timelines import UserTimelineItem
from ninetyseven.apps.relationships.models import *

site = Site.objects.get(id=settings.SITE_ID)
site_url = "http://%s/" % site.domain

class LatestUserTimelineItemsForFollowing(Feed):
  """ A feed of the latest UserTimelineItem objects added to the site by the people a particular user is following. """

  title_template = 'timelines/feeds/item_title.html'
  description_template = 'timelines/feeds/item_description.html'

  link = site_url
  description = "The latest timeline items added at %s" % site.name

  def get_object(self, bits):
    username = bits[0]
    try:
      return User.objects.get(username=username)
    except ValueError:
        raise FeedDoesNotExist

  def title(self, obj):
    try:
      # If Savoy's profile app is installed, use the profile name.
      return "%s: Activity for people %s is following" % (site.name, obj.profile.name.encode("utf-8"))
    except:
      # If not, just use the username
      return "%s: Activity for people %s is following" % (site.name, obj.username)

  def items(self, obj):
    following_relationships = Relationship.objects.filter(from_user=obj)
    following_users = [ relationship.to_user for relationship in following_relationships ]
    return UserTimelineItem.objects.filter(user__in=following_users)[:15]

  def item_pubdate(self, item):
      return item.timestamp

  def item_author_name(self, item):
    try:
      return item.user.profile.name.encode("utf-8")
    except:
      return item.user.username

  def item_link(self, item):
    try:
      return item.get_absolute_url()
    except:
      return ""

  def item_author_email(self, item):
    return ""

  def item_author_link(self, item):
    try:
      # Try to return Savoy's profile app's user profile, first
      return item.user.profile.get_absolute_url()
    except:
      # If Savoy's profile app isn't present, just return None
      return None