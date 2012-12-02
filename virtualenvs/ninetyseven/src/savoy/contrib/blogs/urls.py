from django.contrib.syndication.views import feed
from django.conf import settings
from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from django.views.generic.list_detail import object_list
from django.views.generic.date_based import *

from savoy.contrib.blogs.models import *
from savoy.contrib.blogs.views import *
from savoy.contrib.blogs.feeds import *


entry_archive = {
  'queryset': Entry.objects.all(),
  'date_field': 'date_published',
  'allow_empty': True,
  'template_object_name': 'entry',
  'extra_context': {'entry_filter': 'all'},
}

featured_entry_archive = {
  'queryset': Entry.objects.filter(featured=True),
  'date_field': 'date_published',
  'allow_empty': True,
  'template_object_name': 'entry',
  'extra_context': {'entry_filter': 'featured'},
}

blog_list = {
  'queryset': Blog.objects.all(),
  'allow_empty': True,
  'template_object_name': 'blog',
  'paginate_by': 20,  
}

if not settings.USE_SINGLE_BLOG_URLS:
  urlpatterns = patterns('',
    # Blog list.
    url(
      regex   = '^$',
      view    = object_list,
      name    = 'blog_list',
      kwargs  = blog_list,
    ),
    # Archive of all entries, regardless of blog.
    url(
      regex   = '^all-entries/$',
      view    = archive_index,
      name    = 'all_entries_archive_index',
      kwargs  = dict(entry_archive,
                  num_latest = 30,
                  template_object_name = 'entries',
                  template_name = 'blogs/combined_entry_archive.html',
                )
    ),
    url(
      regex   = '^all-entries/(?P<year>\d{4})/$',
      view    = archive_year,
      name    = 'all_entries_archive_year',
      kwargs  = dict(entry_archive, 
                  make_object_list = True,
                  template_name = 'blogs/combined_entry_archive_year.html',
                ),
    ),
    url(
      regex   = '^all-entries/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
      view    = archive_month,
      name    = 'all_entries_archive_month',
      kwargs  = dict(entry_archive,
                  template_name = 'blogs/combined_entry_archive_month.html',
                ),
    ),
    url(
      regex   = '^all-entries/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/$',
      view    = archive_day,
      name    = 'all_entries_archive_day',
      kwargs  = dict(entry_archive,
                  template_name = 'blogs/combined_entry_archive_day.html',
                ),
    ),
    # Archive of all featured entries, regardless of blog.
    url(
      regex   = '^featured-entries/$',
      view    = archive_index,
      name    = 'featured_entries_archive_index',
      kwargs  = dict(featured_entry_archive,
                  num_latest = 30,
                  template_object_name = 'entries',
                  template_name = 'blogs/combined_entry_archive.html',
                )
    ),
    url(
      regex   = '^featured-entries/(?P<year>\d{4})/$',
      view    = archive_year,
      name    = 'featured_entries_archive_year',
      kwargs  = dict(featured_entry_archive, 
                  make_object_list = True,
                  template_name = 'blogs/combined_entry_archive_year.html',
                ),
    ),
    url(
      regex   = '^featured-entries/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
      view    = archive_month,
      name    = 'featured_entries_archive_month',
      kwargs  = dict(featured_entry_archive,
                  template_name = 'blogs/combined_entry_archive_month.html',
                ),
    ),
    url(
      regex   = '^featured-entries/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/$',
      view    = archive_day,
      name    = 'featured_entries_archive_day',
      kwargs  = dict(featured_entry_archive,
                  template_name = 'blogs/combined_entry_archive_day.html',
                ),
    ),
    # Per-blog archives.
    url(
      regex   = '^(?P<blog_slug>[-\w]+)/$',
      view    = blog_archive_index,
      name    = 'blog_index',
    ),
    url(
      regex   = '^(?P<blog_slug>[-\w]+)/(?P<year>\d{4})/$',
      view    = blog_archive_year,
      name    = 'blog_archive_year',
    ),
    url(
      regex   = '^(?P<blog_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
      view    = blog_archive_month,
      name    = 'blog_archive_month',
    ),
    url(
      regex   = '^(?P<blog_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/$',
      view    = blog_archive_day,
      name    = 'blog_archive_day',
    ),
    # Blog entry permalink.
    url(
      regex   = '^(?P<blog_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$',
      view    = blog_entry_detail,
      name    = 'blog_entry_detail',
    ),
  )
else:
  urlpatterns = patterns('',
    url(
      regex   = '^$',
      view    = blog_archive_index,
      name    = 'blog_index',
    ),
    url(
      regex   = '^(?P<year>\d{4})/$',
      view    = blog_archive_year,
      name    = 'blog_archive_year',
    ),
    url(
      regex   = '^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
      view    = blog_archive_month,
      name    = 'blog_archive_month',
    ),
    url(
      regex   = '^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/$',
      view    = blog_archive_day,
      name    = 'blog_archive_day',
    ),
    url(
      regex   = '^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$',
      view    = blog_entry_detail,
      name    = 'blog_entry_detail',
    ),
  )


# URLs for feeds...

feeds = {
  'latest-entries':     LatestEntries,
  'entries':            LatestEntriesPerBlog,
  'comments-for-entry': LatestCommentsPerEntry,
}


urlpatterns += patterns('',
  url(
    regex   = '^feeds/(?P<url>.*)/$',
    view    = feed,
    kwargs  = { 'feed_dict': feeds },
    name    = 'blog_feeds',
  )
)