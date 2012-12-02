from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list
from django.contrib.syndication.views import feed

from savoy.contrib.podcasts.views import *
from savoy.contrib.podcasts.models import Episode, Show
from savoy.contrib.podcasts.feeds import *

show_list = {
  'queryset': Show.objects.all(),
  'allow_empty': True,
  'template_object_name': 'show',
}

urlpatterns = patterns('',
  url(
    regex   = '^$',
    view    = object_list,
    name    = 'show_list',
    kwargs  = show_list,
  ),
  url(
    regex   = '^(?P<slug>[-\w]+)/$',
    view    = show_detail,
    name    = 'show_detail',
  ),
  url(
    regex   = '^(?P<show_slug>[-\w]+)/(?P<year>\d{4})/$',
    view    = episode_archive,
    name    = 'episode_archive_year',
  ),
  url(
    regex   = '^(?P<show_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
    view    = episode_archive,
    name    = 'episode_archive_month',
  ),
  url(
    regex   = '^(?P<show_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/$',
    view    = episode_archive,
    name    = 'episode_archive_day',
  ),
  url(
    regex   = '^(?P<show_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$',
    view    = episode_detail,
    name    = 'episode_detail',
  ),
)

# URLs for feeds...

feeds = {
  'latest-episodes': LatestEpisodes,
  'episodes-for-show': LatestEpisodesPerShow,
}


urlpatterns += patterns('',
  url(
    regex   = '^feeds/(?P<url>.*)/$',
    view    = feed,
    kwargs  = { 'feed_dict': feeds },
    name    = 'podcast_feeds',
  )
)