import datetime
import time

from django.conf import settings
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType

from savoy.contrib.aggregator.models import ContentItem


site = Site.objects.get(id=settings.SITE_ID)
site_url = "http://%s/" % site.domain



class LatestItems(Feed):
  """ A feed of the latest ContentItem objects. """
  
  title_template = 'aggregator/feeds/item_title.html'
  description_template = 'aggregator/feeds/item_description.html'
  
  title = "%s: Latest items" % site.name
  link = site_url
  description = "The latest items at %s" % site.name

  def items(self):
    from savoy.contrib.aggregator.views import get_aggregator_content_types, filter_queryset_by_model_list, filter_view_by_models
    queryset = ContentItem.objects.all().order_by('-timestamp')
    model_list = self.request.GET.get('models', 'default')
    queryset, content_types = filter_queryset_by_model_list(queryset, model_list)
    return queryset[:35]

  def item_pubdate(self, item):
    return item.timestamp
  
  def item_link(self, item):
    try:
      return item.content_object.parent_object().get_absolute_url()
    except:
      return item.get_absolute_url()
  
  item_author_name = ""
  item_author_email = ""
  item_author_link = ""