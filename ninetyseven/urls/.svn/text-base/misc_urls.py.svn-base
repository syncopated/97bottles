from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from ninetyseven.views import *

urlpatterns = patterns('',
  url(
    regex   = r'^$',
    view    = homepage,
    name    = "homepage",
  ),
  url(
    regex   = '^find_friends/twitter/$',
    view    = find_twitter_friends,
    name    = 'find_twitter_friends',
  ),
  url(
    regex   = r'^cities/_search/$',
    view    = search_cities,
    name    = 'search_cities',
  ),
)