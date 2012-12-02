from django.conf.urls.defaults import *
from django.contrib.contenttypes.models import ContentType

from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication

from faves.models import *

from ninetyseven.apps.api.handlers import *
from ninetyseven.apps.beers.models import *

auth = HttpBasicAuthentication(realm='97Bottles API')

beers                 = Resource(handler=BeerHandler, authentication=auth)
beers_recommended_for = Resource(handler=BeerRecommendedForHandler, authentication=auth)
beers_fave_list       = Resource(handler=BeerFaveListHandler, authentication=auth)
breweries             = Resource(handler=BreweryHandler, authentication=auth)

urlpatterns = patterns('',
  # Beers
  url(
    regex   = r'^beers/$',
    view    = beers,
    name    = 'api_beer_list',
  ),
  url(
    regex   = r'^beers/(?P<id>\d+)/$',
    view    = beers,
    name    = 'api_beer_detail',
  ),
  url(
    regex   = r'^beers/(?P<created_by__username>[-\w]+)/created/$',
    view    = beers,
    name    = 'api_beers_created_by',
  ),
  url(
    regex   = r'^beers/(?P<username>[-\w]+)/recommended/$',
    view    = beers_recommended_for,
    name    = 'api_beers_recommended_for',
  ),
  url(
    regex   = r'^beers/(?P<username>[-\w]+)/(?P<fave_type_slug>[-\w]+)/$',
    view    = beers_fave_list,
    name    = 'api_beers_fave_list',
  ),
  
  # Breweries
  url(
    regex   = r'^breweries/$',
    view    = breweries,
    name    = 'api_brewery_list',
  ),
  url(
    regex   = r'^breweries/(?P<id>\d+)/$',
    view    = breweries,
    name    = 'api_brewery_detail',
  ),
  url(
    regex   = r'^breweries/(?P<created_by__username>[-\w]+)/created/$',
    view    = breweries,
    name    = 'api_breweries_created_by',
  ),
)