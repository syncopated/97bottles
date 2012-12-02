from django.http import Http404
from django.template.defaultfilters import slugify, dictsortreversed
from django.contrib.localflavor.us.us_states import STATE_CHOICES
from django.views.decorators.cache import cache_page

from savoy.core.constants import COUNTRY_CHOICES
from savoy.core.geo.models import *
from savoy.utils.date_sort import *

def location_index(request):
  from django.views.generic.list_detail import object_list
  cities = City.objects.all()
  
  city_list = []
  if 'savoy.contrib.aggregator' in settings.INSTALLED_APPS:
    for city in cities:
      if len(city.aggregator_items()) > 0:
        city_list.append(city)
  else:
    city_list = cities
  
  extra_context = {'city_list': city_list, }
  
  return object_list(
    request, 
    queryset = cities,
    template_name = 'geo/location_index.html',
    template_object_name = 'all_city',
    allow_empty = True,
    extra_context = extra_context,
  )

def country_detail(request, country):
  from django.views.generic.list_detail import object_list
  try:
    cities = City.objects.filter(country=country)
  except:
    raise Http404
  for country_code in COUNTRY_CHOICES:
    if country_code[0] == country:
      country_name = country_code[1]
  extra_context = {
    'country': country_name,
    'country_code': country.upper()
  }
  return object_list(
    request, 
    queryset = cities,
    template_name = 'geo/country_detail.html',
    template_object_name = 'city',
    allow_empty = False,
    extra_context = extra_context,
  )

def state_detail(request, country, state):
  from django.views.generic.list_detail import object_list

  cities = City.objects.filter(slug__endswith=slugify(state + " " + country))
  
  try:
    # This needs to raise n exception on things like /ca/vancouver, but not on /ca/bc/vancouver.
    if slugify(cities[0].city) == state:
      raise Exception
  except:
    try:
      # If not, this is probably supposed to be a city view, not a state view.
      city = state
      return city_detail(request=request, country=country, city=city)
    except:
      raise Http404
    
  country_name  = cities[0].get_country_display()
  country_code  = cities[0].country
  if country == "us":
    state_name  = cities[0].get_state_display()
    state_code  = cities[0].state
  else:
    state_name  = cities[0].province
    state_code  = slugify(cities[0].province)

  extra_context = {
    'country': country_name,
    'country_code': country_code,
    'state': state_name,
    'state_code': state_code,
  }
  
  return object_list(
    request, 
    queryset = cities,
    template_name = 'geo/state_detail.html',
    template_object_name='city',
    allow_empty=True,
    extra_context = extra_context,
  )

def city_detail(request, country, city, state=None, allow_empty=True):
  from django.views.generic.list_detail import object_detail
  
  # Find the city we're dealing with based on its slug.
  if state:
    slug = slugify(city + " " + state + " " + country)
  else:
    slug = slugify(city + " " + country)
  try:
    city = City.objects.get(slug=slug)
  except:
    raise Http404

  # Get the city and state name and code for inclusion in our template context.
  country_name  = city.get_country_display()
  country_code  = city.country
  if country == "us":
    state_name  = city.get_state_display()
    state_code  = city.state
  else:
    state_name  = city.province
    state_code  = slugify(city.province)


  if "savoy.contrib.aggregator" in settings.INSTALLED_APPS:
    object_list = dictsortreversed(city.aggregator_items(), 'timestamp')
  else:
    object_list = sort_items_by_date(city.items(), recent_first=True)
    
  extra_context = {
    'country': country_name,
    'country_code': country_code,
    'state': state_name,
    'state_code': state_code,
    'object_list': object_list,
  }

  # Render a generic detail view.
  return object_detail(
    request, 
    queryset = City.objects.all(),
    template_name = 'geo/city_detail.html',
    template_object_name='city',
    slug_field = 'slug',
    slug = slug,
    extra_context = extra_context,
  )   
  

def neighborhood_detail(request, country, city, neighborhood_slug, state=None, allow_empty=True):
  from django.views.generic.list_detail import object_detail

  if state:
    slug = slugify(city + " " + state + " " + country)
  else:
    slug = slugify(city + " " + country)
  try:
    city = City.objects.get(slug=slug)
  except:
    raise Http404

  try:
    neighborhood = Neighborhood.objects.get(city=city, slug=neighborhood_slug)
  except:
    raise Http404

  if "savoy.contrib.aggregator" in settings.INSTALLED_APPS:
    object_list = dictsortreversed(neighborhood.aggregator_items(), 'timestamp')
  else:
    object_list = sort_items_by_date(neighborhood.items(), recent_first=True)

  extra_context = {
    'object_list' : object_list,
  }


  return object_detail(
    request, 
    queryset = Neighborhood.objects.filter(city=city),
    template_name = 'geo/neighborhood_detail.html',
    template_object_name='neighborhood',
    slug_field = 'slug',
    slug = neighborhood_slug,
    extra_context = extra_context,
  )


def place_detail(request, country, city, place_slug, state=None, allow_empty=True):
  from django.views.generic.list_detail import object_detail
  if state:
    slug = slugify(city + " " + state + " " + country)
  else:
    slug = slugify(city + " " + country)
  try:
    city = City.objects.get(slug=slug)
  except:
    raise Http404
  
  try:
    place = Place.objects.get(city=city, slug=place_slug)
  except:
    raise Http404
  
  if "savoy.contrib.aggregator" in settings.INSTALLED_APPS:
    object_list = dictsortreversed(place.aggregator_items(), 'timestamp')
  else:
    object_list = sort_items_by_date(place.items(), recent_first=True)

  extra_context = {
    'object_list' : object_list,
  }
  
  return object_detail(
    request, 
    queryset = Place.objects.filter(city=city),
    template_name = 'geo/place_detail.html',
    template_object_name='place',
    slug_field = 'slug',
    slug = place_slug,
    extra_context = extra_context,
  )