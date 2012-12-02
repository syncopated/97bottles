from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.localflavor.us.us_states import STATE_CHOICES

from geopy import geocoders

from savoy.core.constants import COUNTRY_CHOICES
from savoy.core.geo.utils.urban_mapping_client import UrbanMappingClient


def get_location_from_address(address):
  g = geocoders.Google(settings.GOOGLE_MAPS_API_KEY)
  try:
    locations = list(g.geocode(address, exactly_one=False))
    first_location = locations[0]
    return first_location[1]
  except:
    return None

def get_city_from_flickr(latitude, longitude):
  from savoy.core.geo.models import City
  import flickrapi
  try:
    flickr = flickrapi.FlickrAPI(settings.FLICKR_API_KEY, settings.FLICKR_API_SECRET)
    city = None
    try:
      flickr_place_id = flickr.places_findByLatLon(lat=latitude, lon=longitude).places[0].place[0]['place_id']
      flickr_place = flickr.places_resolvePlaceId(place_id=flickr_place_id).location[0]
    except:
      raise

    # Find the various city bits.
    try:
      country = flickr_place.country[0].elementText
    except:
      country = None
    try:
      city_name = flickr_place.locality[0].elementText.split(',')[0]
    except:
      city_name = None
    try:
      county = flickr_place.county[0].elementText.split(',')[0].strip(" County")
    except:
      county = ''
    try:
      state = flickr_place.region[0].elementText.split(',')[0]
      state_code = None
    except:
      state = None
      state_code = None

    # Build and save the city object.
    country_code = None
  
    if country and city_name:
      # Look up our country name in COUNTRY_CHOICES to find the country code.
      for item in COUNTRY_CHOICES:
        if item[1] == country:
          country_code = item[0]
        
          # If the country is United States, look up the state in STATE_CHOICES
          if country_code == 'us':
            for item in STATE_CHOICES:
              if item[1] == state:
                state_code = item[0]
            province = ''
            slug = slugify(city_name + " " + state_code  + " " + 'us')
    
          # If the country is other than United State, use the "province" field, instead.
          else:
            province = state
            state = ''
            slug = slugify(city_name + " " + province  + " " + country_code)
    
      # If we've gotten this far, we can build a City object.
      if country_code and city_name:
        try:
          if country_code == 'us':
            city = City.objects.get(city=city_name, state=state_code, country='us')
          else:
            city = City.objects.get(city=city_name, province=province, country=country_code)
        except:
          if country_code == 'us':
            city = City(city=city_name, state=state_code, country='us', slug=slug)
          else:
            city = City(city=city_name, province=province, country=country_code, slug=slug)
          city.county = county
          city.save()

    # Finally, return the city.
    if city:
      return city
    else:
      return None
  except:
    raise
    return None
    
    
def get_neighborhood_from_urban_mapping(latitude, longitude, city=None):
  from savoy.core.geo.models import Neighborhood, City
  neighborhood = None
  try:
    if not city:
      city = get_city_from_flickr(latitude, longitude)
    urban_mapping_api = UrbanMappingClient(method="getNeighborhoodsByLatLng")
    params = {
      'apikey'    : settings.URBAN_MAPPING_API_KEY,
      'lat'       : latitude,
      'lng'       : longitude,
      'results'   : 'one',
    }
    neighborhoods = urban_mapping_api(**params)
    for neighborhood in neighborhoods.getiterator('neighborhood'):
      try:          
        # The name tends to have crazy whitespace in it. Strip it out!
        neighborhood_name = neighborhood.find('name').text.replace('  ', '').replace('\n', '').replace('\t', '')
        # Get or save the neighborhood
        neighborhood, created = Neighborhood.objects.get_or_create(
          name = neighborhood_name,
          slug = slugify(neighborhood.find('name').text),
          city = city,
        )
        if created:
          neighborhood.save()
      except:
        raise
  except:
    raise
  return neighborhood