from django.conf.urls.defaults import *
from django.views.generic.date_based import *
from django.contrib.syndication.views import feed

from savoy.contrib.statuses.models import *
from savoy.contrib.statuses.feeds import *

status_archive = {
  'queryset': Status.objects.all(),
  'date_field': 'date_published',
  'allow_empty': True,
  'template_object_name': 'status',
}

status_detail = {
  'queryset': Status.objects.all(),
  'date_field': 'date_published',
  'template_object_name': 'status',
}

urlpatterns = patterns('',
    url(
      regex   = '^$',
      view    = archive_index,
      name    = 'status_index',
      kwargs  = dict(status_archive,
                  num_latest = 30,
                  template_object_name = 'statuses',
                )
    ),
    url(
      regex   = '^(?P<year>\d{4})/$',
      view    = archive_year,
      name    = 'status_archive_year',
      kwargs  = dict(status_archive, 
                  make_object_list = True,
                ),
    ),
    url(
      regex   = '^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
      view    = archive_month,
      name    = 'status_archive_month',
      kwargs  = status_archive,
    ),
    url(
      regex   = '^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/$',
      view    = archive_day,
      name    = 'status_archive_day',
      kwargs  = status_archive,
    ),
    url(
      regex   = '^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/(?P<object_id>\d+)/$',
      view    = object_detail,
      name    = 'status_detail',
      kwargs  = status_detail,
    ),

)

# URLs for feeds...

feeds = {
  'latest-statuses': LatestStatuses,
}


urlpatterns += patterns('',
  url(
    regex   = '^feeds/(?P<url>.*)/$',
    view    = feed,
    kwargs  = { 'feed_dict': feeds },
    name    = 'statuses_feeds',
  )
)