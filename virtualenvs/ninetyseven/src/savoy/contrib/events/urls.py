from django.conf.urls.defaults import *
from django.views.generic.date_based import archive_index, archive_year, archive_month, archive_day
from django.views.generic.list_detail import object_detail

from savoy.contrib.events.models import *
from savoy.contrib.events.views import *

eventtime_archive = {
  'queryset': EventTime.objects.all().select_related(),
  'date_field': 'start_time',
  'allow_empty': True,
  'allow_future': True,
  'template_object_name': 'eventtime',
}

event_detail = {
  'queryset': Event.objects.all().select_related(),
  'template_object_name': 'event',
}

urlpatterns = patterns('',
    url(
      regex   = '^$',
      view    = archive_index,
      name    = 'eventtime_index',
      kwargs  = dict(eventtime_archive,
                      num_latest = 30,
                      template_object_name = 'latest',
                    )
    ),
    url(
      regex   = '^(?P<year>\d{4})/$',
      view    = archive_year,
      name    = 'eventtime_archive_year',
      kwargs  = dict(eventtime_archive,
                     make_object_list = True,
                    )
    ),
    url(
      regex   = '^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
      view    = archive_month,
      name    = 'eventtime_archive_month',
      kwargs  = eventtime_archive,
    ),
    url(
      regex   = '^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/$',
      view    = archive_day,
      name    = 'eventtime_archive_day',
      kwargs  = eventtime_archive,
    ),
    url(
      regex   = '^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/(?P<eventtime_id>\d+)/$',
      view    = eventtime_detail,
      name    = 'eventtime_detail',
    ),
    url(
      regex   = '^(?P<object_id>\d+)/$',
      view    = object_detail,
      name    = 'event_detail',
      kwargs  = event_detail,
    ),
)