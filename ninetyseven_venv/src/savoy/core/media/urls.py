from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.date_based import *
from django.contrib.syndication.views import feed

from savoy.core.media.models import *
from savoy.core.media.feeds import *

try:
  photo_queryset = Photo.objects.filter(flickrphoto__owner__nsid=settings.FLICKR_USERID)
  photo_favorite_queryset = Photo.objects.exclude(flickrphoto__owner__nsid=settings.FLICKR_USERID)
except:
  photo_queryset = Photo.objects.all()
  photo_favorite_queryset = None

# URLs for photos

photo_archive = {
  'queryset': photo_queryset,
  'date_field': 'date_published',
  'allow_empty': True,
  'template_object_name': 'photo',
  'extra_context': { 'photo_type': 'non-favorite' },
}

photo_detail = {
  'queryset': photo_queryset,
  'date_field': 'date_published',
  'template_object_name': 'photo',
  'slug_field': 'slug',
  'template_name': 'media/photos/photo_detail.html',
  'extra_context': { 'photo_type': 'non-favorite' },
}


urlpatterns = patterns('',
  url(
    regex   = '^photos/$',
    view    = archive_index,
    name    = 'photo_index',
    kwargs  = dict(photo_archive,
                num_latest = 30,
                template_name = "media/photos/photo_archive.html",
                template_object_name = 'latest',
              )
  ),
  url(
    regex   = '^photos/(?P<year>\d{4})/$',
    view    = archive_year,
    name    = 'photo_archive_year',
    kwargs  = dict(photo_archive, 
                make_object_list = True,
                template_name = "media/photos/photo_archive_year.html",
              ),
  ),
  url(
    regex   = '^photos/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
    view    = archive_month,
    name    = 'photo_archive_month',
    kwargs  = dict(photo_archive, 
                template_name = "media/photos/photo_archive_month.html",
              ),
  ),
  url(
    regex   = '^photos/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/$',
    view    = archive_day,
    name    = 'photo_archive_day',
    kwargs  = dict(photo_archive,
                template_name = "media/photos/photo_archive_day.html",
              ),
  ),
  url(
    regex   = '^photos/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
    view    = object_detail,
    name    = 'photo_detail',
    kwargs  = photo_detail,
  ),
)

# URLs for feeds...

feeds = {
  'latest-photos':      LatestPhotos,
}


urlpatterns += patterns('',
  url(
    regex   = '^photos/feeds/(?P<url>.*)/$',
    view    = feed,
    kwargs  = { 'feed_dict': feeds }
  )
)

#URL photo photo detail, in a gallery. Only if galleries is installed:
if 'savoy.contrib.galleries' in settings.INSTALLED_APPS:
  from savoy.contrib.galleries.views import gallery_photo_detail
  urlpatterns += patterns('',
    url(
      regex   = '^photos/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/(?P<photo_slug>[-\w]+)/in-gallery/(?P<gallery_slug>[-\w]+)/$',
      view    = gallery_photo_detail,
      name    = 'gallery_photo_detail',
    ),
  )


# URLs for Flickr favorites

photo_favorite_archive = {
  'queryset': photo_favorite_queryset,
  'date_field': 'date_published',
  'allow_empty': True,
  'template_object_name': 'photo',
  'extra_context': { 'photo_type': 'favorite' },
}

photo_favorite_detail = {
  'queryset': photo_favorite_queryset,
  'date_field': 'date_published',
  'template_object_name': 'photo',
  'slug_field': 'slug',
  'template_name': 'media/photos/photo_detail.html',
  'extra_context': { 'photo_type': 'favorite' },
}

urlpatterns += patterns('',
  url(
    regex   = '^photos/favorites/$',
    view    = archive_index,
    name    = 'photo_favorite_index',
    kwargs  = dict(photo_favorite_archive,
                num_latest = 30,
                template_name = "media/photos/photo_archive.html",
                template_object_name = 'latest',
              )
  ),
  url(
    regex   = '^photos/favorites/(?P<year>\d{4})/$',
    view    = archive_year,
    name    = 'photo_favorite_archive_year',
    kwargs  = dict(photo_favorite_archive, 
                make_object_list = True,
                template_name = "media/photos/photo_archive_year.html",
              ),
  ),
  url(
    regex   = '^photos/favorites/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
    view    = archive_month,
    name    = 'photo_favorite_archive_month',
    kwargs  = dict(photo_favorite_archive, 
                template_name = "media/photos/photo_archive_month.html",
              ),
  ),
  url(
    regex   = '^photos/favorites/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/$',
    view    = archive_day,
    name    = 'photo_favorite_archive_day',
    kwargs  = dict(photo_favorite_archive,
                template_name = "media/photos/photo_archive_day.html",
              ),
  ),
  url(
    regex   = '^photos/favorites/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
    view    = object_detail,
    name    = 'photo_favorite_detail',
    kwargs  = photo_favorite_detail,
  ),
)


# URLs for feeds...

favorites_feeds = {
  'latest-photos':      LatestFavoritePhotos,
}


urlpatterns += patterns('',
  url(
    regex   = '^photos/favorites/feeds/(?P<url>.*)/$',
    view    = feed,
    kwargs  = { 'feed_dict': favorites_feeds }
  )
)
  
  
# URLs for embedded media

embedded_media_archive = {
  'queryset': EmbeddedMedia.objects.all(),
  'date_field': 'date_published',
  'allow_empty': True,
  'template_object_name': 'embeddedmedia',
}

embedded_media_detail = {
  'queryset': EmbeddedMedia.objects.all(),
  'date_field': 'date_published',
  'template_object_name': 'embeddedmedia',
  'slug_field': 'slug',
  'template_name': 'media/embedded/embedded_media_detail.html',
}


urlpatterns += patterns('',
  url(
    regex   = '^embedded/$',
    view    = archive_index,
    name    = 'embedded_media_index',
    kwargs  = dict(embedded_media_archive,
                num_latest = 30,
                template_name = "media/embedded/embedded_media_archive.html",
                template_object_name = 'latest',
              )
  ),
  url(
    regex   = '^embedded/(?P<year>\d{4})/$',
    view    = archive_year,
    name    = 'embedded_media_archive_year',
    kwargs  = dict(embedded_media_archive, 
                make_object_list = True,
                template_name = "media/embedded/embedded_media_archive_year.html",
              ),
  ),
  url(
    regex   = '^embedded/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
    view    = archive_month,
    name    = 'embedded_media_archive_month',
    kwargs  = dict(embedded_media_archive, 
                template_name = "media/embedded/embedded_media_archive_month.html",
              ),
  ),
  url(
    regex   = '^embedded/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/$',
    view    = archive_day,
    name    = 'embedded_media_archive_day',
    kwargs  = dict(embedded_media_archive,
                template_name = "media/embedded/embedded_media_archive_day.html",
              ),
  ),
  url(
    regex   = '^embedded/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
    view    = object_detail,
    name    = 'embedded_media_detail',
    kwargs  = embedded_media_detail,
  ),
)
