from django.conf.urls.defaults import *
from django.views.generic.date_based import *
from django.contrib.syndication.views import feed

from savoy.contrib.bookmarks.models import *
from savoy.contrib.bookmarks.feeds import *

bookmark_archive = {
  'queryset': Bookmark.objects.all(),
  'date_field': 'date_published',
  'allow_empty': True,
  'template_object_name': 'bookmark',
}

bookmark_detail = {
  'queryset': Bookmark.objects.all(),
  'date_field': 'date_published',
  'template_object_name': 'bookmark',
  'slug_field': 'slug',
}

urlpatterns = patterns('',
    url(
      regex   = '^$',
      view    = archive_index,
      name    = 'bookmark_index',
      kwargs  = dict(bookmark_archive,
                  num_latest = 30,
                  template_object_name = 'bookmarks',
                )
    ),
    url(
      regex   = '^(?P<year>\d{4})/$',
      view    = archive_year,
      name    = 'bookmark_archive_year',
      kwargs  = dict(bookmark_archive, 
                  make_object_list = True,
                ),
    ),
    url(
      regex   = '^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
      view    = archive_month,
      name    = 'bookmark_archive_month',
      kwargs  = bookmark_archive,
    ),
    url(
      regex   = '^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/$',
      view    = archive_day,
      name    = 'bookmark_archive_day',
      kwargs  = bookmark_archive,
    ),
    url(
      regex   = '^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
      view    = object_detail,
      name    = 'bookmark_detail',
      kwargs  = bookmark_detail,
    ),

)

# URLs for feeds...

feeds = {
  'latest-bookmarks':       LatestBookmarks,
  'comments-for-bookmark':  LatestCommentsPerBookmark,
}


urlpatterns += patterns('',
  url(
    regex   = '^feeds/(?P<url>.*)/$',
    view    = feed,
    kwargs  = { 'feed_dict': feeds }
  )
)