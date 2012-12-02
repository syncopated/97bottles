from django.conf.urls.defaults import *
 
from ninetyseven.apps.beers.views import *
 
urlpatterns = patterns('',
  url(
    regex = r'^_search/$',
    view = search_breweries,
    name = 'search_breweries',
  ),
  url(
    regex = r'^$',
    view = brewery_index,
    name = 'brewery_index',
    ),
  url(
    regex   = r'^(?P<country>[a-z]{2})/$',
    view    = brewery_country_detail,
    name    = 'country_detail',
  ),
  url(
    regex   = r'^(?P<country>[a-z]{2})/(?P<state>[-\w]+)/$',
    view    = brewery_state_detail,
    name    = 'state_detail',
  ),
  url(
    regex   = r'^(?P<country>[a-z]{2})/(?P<state>[-\w]+)/(?P<city>[-\w]+)/$',
    view    = brewery_city_detail,
    name    = 'city_detail',
  ),
  url(
    regex   = r'^(?P<country>[a-z]{2})/(?P<state>[-\w]+)/(?P<city>[-\w]+)/(?P<brewery_slug>[-\w]+)/$',
    view    = brewery_detail,
    name    = 'brewery_detail',
    ),
  url(
    regex = r'^breweries/_edit/(?P<brewery_id>\d+)/$',
    view = edit_brewery,
    name = 'edit_brewery',
  ),
  url(
    regex   = r'^(?P<country>[a-z]{2})/(?P<state>[-\w]+)/(?P<city>[-\w]+)/(?P<brewery_slug>[-\w]+)/(?P<slug>[-\w]+)/$',
    view    = beer_detail,
    name    = 'beer_detail',
    ),
  url(
    regex   = r'^(?P<country>[a-z]{2})/(?P<state>[-\w]+)/(?P<city>[-\w]+)/(?P<brewery_slug>[-\w]+)/(?P<slug>[-\w]+)/reviews/$',
    view    = reviews_for_beer,
    name    = 'reviews_for_beer',
    ),
)