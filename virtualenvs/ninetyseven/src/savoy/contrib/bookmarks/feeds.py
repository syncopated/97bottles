import datetime
import time

from django.conf import settings
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType

from savoy.contrib.bookmarks.models import Bookmark

site = Site.objects.get(id=settings.SITE_ID)
site_url = "http://%s/" % site.domain



class LatestBookmarks(Feed):
  """ A feed of the latest bookmarks. """
  
  title_template = 'bookmarks/feeds/bookmark_title.html'
  description_template = 'bookmarks/feeds/bookmark_description.html'
  
  title = "%s: Latest bookmarks" % site.name
  link = site_url
  description = "The latest bookmarks at %s" % site.name

  def items(self):
    return Bookmark.live_bookmarks.all().order_by('-date_published')[:15]

  def item_pubdate(self, item):
      return item.date_published

  item_author_name  = ""
  item_author_email = ""
  item_author_link  = ""


  
class LatestCommentsPerBookmark(Feed):
  """Returns a feed of comments on a given content object."""
  title_template = 'comments/feeds/comment_title.html'
  description_template = 'comments/feeds/comment_description.html'
  
  link = site_url
  description = "The latest comment at %s" % site.name

  def get_object(self, bits):
    try:
      year  = bits[0]
      month = bits[1]
      day   = bits[2]
      slug  = bits[3]
    except:
      raise FeedDoesNotExist

    try:
        date = datetime.date(*time.strptime(year+month+day, '%Y'+'%b'+'%d')[:3])
        return Bookmark.live_bookmarks.get(
          date_published__range = (datetime.datetime.combine(date, datetime.time.min), datetime.datetime.combine(date, datetime.time.max)), 
          slug = slug,
        )

    except ValueError:
        raise FeedDoesNotExist

  def title(self, obj):
    return "%s: Comments on %s" % (site.name, obj.title)

  def items(self, obj):
    from savoy.contrib.comments.models import Comment
    return Comment.approved_comments.filter(content_type=ContentType.objects.get_for_model(Bookmark), object_id=obj.id)[:15]

  def item_author_name(self, item):
    try:
      return item.author_name.encode("utf-8")
    except:
      return 'Unknown'

  def item_link(self, item):
    # This is not quite ideal, because it doesn't add "#cXXXX" to the comment URL.
    return item.parent_object().get_absolute_url()

  def item_author_email(self, item):
    return ""

  def item_author_link(self, item):
    return item.author_url.encode("utf-8")

  def item_pubdate(self, item):
    return item.date_submitted