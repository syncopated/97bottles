from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail

from savoy.core.geo.models import *
from savoy.core.geo.views import *

urlpatterns = patterns('',    
    url(
      regex   = '^$',
      view    = location_index,
      name    = 'location_index',
    ),
    url(
      regex   = '^(?P<country>[a-z]{2})/$',
      view    = country_detail,
      name    = 'country_detail',
    ),
    url(
      regex   = '^(?P<country>[a-z]{2})/(?P<state>[-\w]+)/$',
      view    = state_detail,
      name    = 'state_detail',
    ),
    url(
      regex   = '^(?P<country>[a-z]{2})/(?P<state>[-\w]+)/(?P<city>[-\w]+)/$',
      view    = city_detail,
      name    = 'city_detail',
    ),
    url(
      regex   = '^(?P<country>[a-z]{2})/(?P<state>[-\w]+)/(?P<city>[-\w]+)/places/(?P<place_slug>[-\w]+)/$',
      view    = place_detail,
      name    = 'place_detail',
    ),
    url(
      regex   = '^(?P<country>[a-z]{2})/(?P<state>[-\w]+)/(?P<city>[-\w]+)/neighborhoods/(?P<neighborhood_slug>[-\w]+)/$',
      view    = neighborhood_detail,
      name    = 'neighborhood_detail',
    ),
)
