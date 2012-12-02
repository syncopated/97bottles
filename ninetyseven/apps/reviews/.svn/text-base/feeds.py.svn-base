import datetime
import time

from django.conf import settings
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType

from ninetyseven.apps.reviews.models import Review
from ninetyseven.apps.beers.models import Beer

site = Site.objects.get(id=settings.SITE_ID)
site_url = "http://%s/" % site.domain

class LatestReviews(Feed):
  """ A feed of the latest reviews added to the site. """
  
  title_template = 'reviews/feeds/review_title.html'
  description_template = 'reviews/feeds/review_description.html'
  
  title = "%s: Newest reviews" % site.name
  link = site_url
  description = "The latest reviews added at %s" % site.name

  def items(self):
    return Review.objects.all().order_by('-date_created')[:15]

  def item_pubdate(self, item):
      return item.date_created

  def item_author_name(self, item):
    return item.created_by.profile.name.encode("utf-8")
  
  item_author_email = ""
  
  def item_author_link(self, item):
    try:
      return "http://%s/people/%s/" % (site.domain, item.created_by.username)
    except:
      return None
      
      
class LatestReviewsPerBeer(Feed):
  """ A feed of the latest Review objects added to the site for a particular Beer object. """

  title_template = 'reviews/feeds/review_title.html'
  description_template = 'reviews/feeds/review_description.html'

  link = site_url

  def get_object(self, bits):
    beer_id = bits[0]
    try:
      return Beer.objects.get(id=beer_id)
    except ValueError:
        raise FeedDoesNotExist

  def title(self, obj):
    return u"%s: Review for %s" % (site.name, obj.name)

  def items(self, obj):
    return Review.objects.filter(beer=obj).order_by('-date_created')

  def item_pubdate(self, item):
      return item.date_created

  def item_author_name(self, item):
    return item.created_by.profile.name.encode("utf-8")

  def item_link(self, item):
    try:
      return item.get_absolute_url()
    except:
      return ""

  def item_author_email(self, item):
    return ""

  def item_author_link(self, item):
    return item.created_by.profile.get_absolute_url()