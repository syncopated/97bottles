import logging
import urllib

from django.conf import settings
from django.utils.encoding import smart_unicode
from django.template.defaultfilters import slugify
from django.contrib.localflavor.us.us_states import STATE_CHOICES

from savoy.core.geo.models import City
from savoy.utils import importers

from ninetyseven.apps.beers.models import Brewery, BreweryType

#
# BeerMapping.com API
#
class BeerMappingClient(object):
    """
    A super-minimal BeerMapping client :)
    """
    def __init__(self, api_key, state):
        self.api_key = api_key
        self.state = state
        
    def __getattr__(self, method):
        return BeerMappingClient(self.api_key, method)
        
    def __repr__(self):
        return "<BeerMappingClient: %s>" % self.method
        
    def __call__(self):
        url = ("http://beermapping.com/webservice/locstate/%s/%s/?" % (self.api_key, self.state))
        return importers.getxml(url)

#
# Public API
#

def enabled():
    return hasattr(settings, 'BEER_MAPPING_API_KEY')
    
def update():
    for state in STATE_CHOICES:
      beer_mapping = BeerMappingClient(settings.BEER_MAPPING_API_KEY, state[0])
      xml = beer_mapping()
      _update_breweries(xml)
                
#
# Private API
#

def _update_breweries(xml):
    for location in xml.getiterator('location'):
        info = dict((k, smart_unicode(location.get(k))) for k in location.keys())
        for e in location.getchildren():
          info[e.tag] = e.text
        _handle_location(info)
        
def _handle_location(info):
    if info['status'] == "Brewery" or info['status'] == "Brewpub":
      city, created = City.objects.get_or_create(
        city = info['city'],
        state = info['state'],
        country = 'us',
      )
      brewery, created = Brewery.objects.get_or_create(
        name = info['name'],
        city = city,
        defaults = dict(
          slug = slugify(info['name']),
          type = BreweryType.objects.get(name="Microbrewery"),
          url = '',
        )
      )
      print brewery
if __name__ == '__main__':
    update()