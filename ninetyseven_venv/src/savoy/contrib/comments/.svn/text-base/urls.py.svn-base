from django.conf.urls.defaults import *
from django.views.generic.date_based import *
from django.contrib.syndication.views import feed

from savoy.contrib.comments.models import *
from savoy.contrib.comments.views import *
from savoy.contrib.comments.feeds import *

comment_archive = {
  'queryset': Comment.approved_comments.all().select_related(),
  'date_field': 'date_submitted',
  'allow_empty': True,
  'template_object_name': 'comment',
}

comment_detail = {
  'queryset': Comment.approved_comments.all().select_related(),
  'date_field': 'date_submitted',
  'template_object_name': 'comment',
}

urlpatterns = patterns('',
    url(
      regex   = '^post/$',
      view    = post_comment
    ),
    url(
      regex   = '^$',
      view    = archive_index,
      name    = 'comment_index',
      kwargs  = dict(comment_archive,
                  num_latest = 30,
                )
    ),
    url(
      regex   = '^(?P<year>\d{4})/$',
      view    = archive_year,
      name    = 'comment_archive_year',
      kwargs  = comment_archive,
    ),
    url(
      regex   = '^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
      view    = archive_month,
      name    = 'comment_archive_month',
      kwargs  = comment_archive,
    ),
    url(
      regex   = '^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/$',
      view    = archive_day,
      name    = 'comment_archive_day',
      kwargs  = comment_archive,
    ),
    url(
      regex   = '^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/(?P<object_id>\d+)/$',
      view    = object_detail,
      name    = 'comment_detail',
      kwargs  = comment_detail,
    ),

)

# URLs for feeds...

feeds = {
  'latest-comments': LatestComments,
}


urlpatterns += patterns('',
  url(
    regex   = '^feeds/(?P<url>.*)/$',
    view    = feed,
    kwargs  = { 'feed_dict': feeds }
  )
)