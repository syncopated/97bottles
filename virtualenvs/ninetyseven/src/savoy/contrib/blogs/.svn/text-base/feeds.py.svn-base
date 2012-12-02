import datetime
import time

from django.conf import settings
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType

from savoy.contrib.blogs.models import Blog, Entry

site = Site.objects.get(id=settings.SITE_ID)
site_url = "http://%s/" % site.domain



class LatestEntries(Feed):
  """ A feed of the latest blog entries, from any blog. """
  
  title_template = 'blogs/feeds/entry_title.html'
  description_template = 'blogs/feeds/entry_description.html'
  
  title = "%s: Latest blog entries" % site.name
  link = site_url
  description = "The latest blog entries at %s" % site.name

  def items(self):
    return Entry.live_entries.all().order_by('-date_published')[:15]

  def item_pubdate(self, item):
      return item.date_published

  def item_author_name(self, item):
    return item.author.name().encode("utf-8")
  
  item_author_email = ""
  
  def item_author_link(self, item):
    try:
      return "http://%s/users/%s/" % (site.domain, item.author.user.username)
    except:
      return None


class LatestEntriesPerBlog(Feed):
  
  title_template = 'blogs/feeds/entry_title.html'
  description_template = 'blogs/feeds/entry_description.html'
  
  def get_object(self, bits):
    if len(bits) != 1:
      raise ObjectDoesNotExist
    return Blog.objects.get(slug=bits[0])

  def title(self, obj):
    return "%s: Latest entries for %s" % (site.name, obj.title)

  def link(self, obj):
    if not obj:
      raise FeedDoesNotExist
    return obj.get_absolute_url()

  def description(self, obj):
    description = "The latest blog entries in %s at %s" % (obj.title, site.name)

  def items(self, obj):
    return Entry.live_entries.filter(blogs=obj).order_by('-date_published')[:15]

  def item_pubdate(self, item):
    return item.date_published

  def item_author_name(self, item):
    try:
      return item.author.name.encode("utf-8")
    except:
      return None
  item_author_email = ""

  def item_author_link(self, item):
    try:
      return "http://%s/users/%s/" % (site.domain, item.author.user.username)      
    except:
      return None

  
class LatestCommentsPerEntry(Feed):
  """Returns a feed of comments on a given content object."""
  title_template = 'comments/feeds/comment_title.html'
  description_template = 'comments/feeds/comment_description.html'
  
  link = site_url
  description = "The latest comment at %s" % site.name

  def get_object(self, bits):
    try:
      if settings.USE_SINGLE_BLOG_URLS:
        blog =  Blog.objects.all()[0]
        year  = bits[0]
        month = bits[1]
        day   = bits[2]
        slug  = bits[3]
      else:
        blog =  Blog.objects.get(slug=bits[0])
        year  = bits[1]
        month = bits[2]
        day   = bits[3]
        slug  = bits[4]
    except:
      raise FeedDoesNotExist
    
    try:
        date = datetime.date(*time.strptime(year+month+day, '%Y'+'%b'+'%d')[:3])
        return Entry.live_entries.get(
          date_published__range = (datetime.datetime.combine(date, datetime.time.min), datetime.datetime.combine(date, datetime.time.max)), 
          slug  = slug,
          blogs = blog,
        )
        
    except ValueError:
        raise FeedDoesNotExist

  def title(self, obj):
    return "%s: Comments on %s" % (site.name, obj.title)

  def items(self, obj):
    from savoy.contrib.comments.models import Comment
    return Comment.approved_comments.filter(content_type=ContentType.objects.get_for_model(Entry), object_id=obj.id)[:15]

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