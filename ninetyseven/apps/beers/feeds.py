import datetime
import time

from django.conf import settings
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType

from ninetyseven.apps.beers.models import Beer, Brewery

site = Site.objects.get(id=settings.SITE_ID)
site_url = "http://%s/" % site.domain

class LatestBeers(Feed):
  """ A feed of the latest beers added to the site. """
  
  title_template = 'beers/feeds/beer_title.html'
  description_template = 'beers/feeds/beer_description.html'
  
  title = "%s: Newest beers" % site.name
  link = site_url
  description = u"The latest beers added at %s" % site.name

  def items(self):
    return Beer.objects.all().order_by('-date_created')[:15]

  def item_pubdate(self, item):
      return item.date_created

  def item_author_name(self, item):
    return item.created_by.profile.name.encode("utf-8")
  
  item_author_email = ""
  
  def item_link(self, item):
    try:
      return item.get_absolute_url()
    except:
      return ""
    
  def item_author_link(self, item):
    try:
      return item.created_by.profile.get_absolute_url()
    except:
      return None
      
class LatestBreweries(Feed):
  """ A feed of the latest breweries added to the site. """

  title_template = 'breweries/feeds/brewery_title.html'
  description_template = 'breweries/feeds/brewery_description.html'

  title = u"%s: Newest breweries" % site.name
  link = site_url
  description = u"The latest breweries added at %s" % site.name

  def items(self):
    return Brewery.objects.all().order_by('-date_created')[:15]

  def item_pubdate(self, item):
      return item.date_created

  def item_author_name(self, item):
    return item.created_by.profile.name.encode("utf-8")

  item_author_email = ""

  def item_link(self, item):
    try:
      return item.get_absolute_url()
    except:
      return ""

  def item_author_link(self, item):
    try:
      return item.created_by.profile.get_absolute_url()
    except:
      return None
      
      
class LatestBeersPerBrewery(Feed):
  """ A feed of the latest Beers objects added to the site for a particular Brewery object. """

  title_template = 'beers/feeds/beers_title.html'
  description_template = 'beers/feeds/beer_description.html'

  link = site_url

  def get_object(self, bits):
    brewery_id = bits[0]
    try:
      return Brewery.objects.get(id=brewery_id)
    except ValueError:
        raise FeedDoesNotExist

  def title(self, obj):
    return u"%s: Beers for %s" % (site.name, obj.name)

  def items(self, obj):
    return Beer.objects.filter(brewery=obj).order_by('-date_created')

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