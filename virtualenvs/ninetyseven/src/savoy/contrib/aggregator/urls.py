from django.conf.urls.defaults import *
from django.contrib.syndication.views import feed

from savoy.contrib.aggregator.views import *
from savoy.contrib.aggregator.feeds import *

urlpatterns = patterns('',
    url(
        regex = "^$",
        view  = archive,
        name  = "aggregator_archive",
    ),
    url(
        regex = "^today/$",
        view  = today,
        name  = "aggregator_today",
    ),
    url(
        regex = "^(?P<year>\d{4})/$",
        view  = year,
        name  = "aggregator_year",
    ),
    url(
        regex = "^(?P<year>\d{4})/(?P<month>\w{3})/$",
        view  = month,
        name  = "aggregator_month",
    ),
    url(
        regex = "^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$",
        view  = day,
        name  = "aggregator_day",
    ),
)

# URLs for feeds...

feeds = {
  'latest-items': LatestItems,
}


urlpatterns += patterns('',
  url(
    regex   = '^feeds/(?P<url>.*)/$',
    view    = feed,
    kwargs  = { 'feed_dict': feeds },
    name    = 'aggregator_feeds',
  )
)