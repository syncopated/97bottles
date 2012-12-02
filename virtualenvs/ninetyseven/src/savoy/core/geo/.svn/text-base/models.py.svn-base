import datetime
from decimal import Decimal

from django.db import models
from django.db.models import permalink, signals
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.localflavor.us.us_states import STATE_CHOICES
from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils.encoding import force_unicode
from tagging.fields import TagField
from django.contrib.localflavor.us.models import USStateField, PhoneNumberField

from savoy.third_party.ascii_dammit import asciiDammit
from savoy.core.constants import COUNTRY_CHOICES
from savoy.core.geo.managers import *

class GeolocatedItem(models.Model):
  """
  Holds the relationship between a geolocation and the item being geolocated.
  """
  latitude            = models.DecimalField(max_digits=11, decimal_places=6)
  longitude           = models.DecimalField(max_digits=11, decimal_places=6)
  city                = models.ForeignKey('City', blank=True, null=True)
  neighborhood        = models.ForeignKey('Neighborhood', blank=True, null=True)
  # place               = models.ForeignKey('Place', blank=True, null=True)
  content_type        = models.ForeignKey(ContentType)
  object_id           = models.PositiveIntegerField()
  content_object      = generic.GenericForeignKey()
  objects             = GeolocatedItemManager()
  

  def __unicode__(self):
    return unicode(self.content_object)
  
  def get_aggregator_content_item(self):
    """ If it exists, returns the aggregator ContentItem object associated with this GeolocatedItem. """
    from savoy.contrib.aggregator.models import ContentItem
    try:
      return ContentItem.objects.get(content_type=self.content_type, object_id=self.object_id)
    except:
      return None

  def get_geolocated_items_within_radius(self, radius_miles=None, content_type=None):
    """ Given a radius in miles (defaults to 1), returns a QuerySet of GeolocatedItem objects within that distance from this GeolocatedItem. """
    if not radius_miles:
      radius_miles = 1
    else:
      radius_miles = Decimal(str(radius_miles))
    radius = Decimal(radius_miles/Decimal("69.04"))
    if content_type:
      items = GeolocatedItem.objects.filter(content_type=content_type, latitude__range=(self.latitude - radius,self.latitude + radius)).filter(longitude__range=(self.longitude - radius,self.longitude + radius))
    else:
      items = GeolocatedItem.objects.filter(latitude__range=(self.latitude - radius,self.latitude + radius)).filter(longitude__range=(self.longitude - radius,self.longitude + radius))
    return items
    
  def get_aggregator_items_within_radius(self, radius_miles=1):
    """ Given a radius in miles (defaults to 1), returns a list of aggregator ContentItem objects within that distance from this GeolocatedItem. """
    geolocated_items = self.get_geolocated_items_within_radius(radius_miles=radius_miles)
    return [ geolocated_item.get_aggregator_content_item() for geolocated_item in geolocated_items if geolocated_item.get_aggregator_content_item() ]
  
  def get_distance_from_location(self, location):
    """ Returns the distance, in miles, between the current GeolocatedItem and another one."""
    import math
    rad = math.pi / 180.0
    y_distance = (float(location.latitude) - float(self.latitude)) * 69.04
    x_distance = (math.cos(float(self.latitude) * rad) + math.cos(float(location.latitude) * rad)) * (float(location.longitude) - float(self.longitude)) * (69.04 / 2)
    distance = math.sqrt( y_distance**2 + x_distance**2 )
    return distance

  def get_closest_place(self):
    """ Returns the Place object nearest this GeolocatedItem. Returns a dictionary with the keys "distance" (in miles) and "place". """
    try:
      return self.get_closest_places()[0]
    except:
      return None

  def get_closest_places(self, mile_limit=25):
    """ 
    Return a dictionary with the keys "distance" (in miles) and "place", sorted by distance ascending.
    Smaller distances are places closer to the this GeolocatedItem. Defaults to only showing places within
    25 miles of the original location. 
    """
    from django.template.defaultfilters import dictsort
    import math
    place_dict_list = []
    for place in Place.objects.all():
      if place != self.content_object:
        if place.location():
          distance = self.get_distance_from_location(place.location())
          if distance <= mile_limit:
            place_dict = { 'distance': float(distance), 'place': place }
            place_dict_list.append(place_dict)
    return dictsort(place_dict_list, 'distance')

  class Meta:
    verbose_name = 'Geolocated Item'
    verbose_name_plural = 'Geolocated Items'
    unique_together = (('latitude', 'longitude', 'content_type', 'object_id'),)


class City(models.Model):
  city            = models.CharField(max_length=100, help_text="Enter the name of the city.")
  state           = USStateField(blank=True, help_text="If USA, select the state.", choices=STATE_CHOICES)
  county          = models.CharField(blank=True, max_length=200, help_text="Enter the name of the county.")
  province        = models.CharField(blank=True, max_length=100, help_text="If not USA, enter province or state here.")
  country         = models.CharField(max_length=100, default='us', help_text="Select the country", choices=COUNTRY_CHOICES,)
  slug            = models.SlugField(unique=True, help_text='The slug is a URL-friendly version of the city name. It is auto-populated.')
  description     = models.TextField(blank=True)

  def __unicode__(self):
    return self.full_name()

  def name(self):
    """ Returns the name of the City in City, State, Province format. """
    return force_unicode(", ".join(b for b in (self.city, self.state, self.province) if b))

  def full_name(self):
    """ Returns the full name of the City in City, State, Province, Country format. """
    return force_unicode(", ".join(b for b in (self.city, self.state, self.province, self.get_country_display()) if b))

  def full_name_ascii(self):
    """ Returns the name of the City in City, State, Province, Country format. Forces ASCII output, which is useful for passing to a geocoder. """
    return force_unicode(", ".join(b for b in (asciiDammit(self.city), asciiDammit(self.state), asciiDammit(self.province), asciiDammit(self.get_country_display())) if b))

  def us_bias_name(self):
    """ If the city is in the USA, returns "Topeka, KS". If it's not, returns, "Sydney, New South Wales, Australia". """
    if self.country == "us":
      return force_unicode(", ".join(b for b in (self.city, self.state) if b))
    else:
      return force_unicode(", ".join(b for b in (self.city, self.state, self.province, self.get_country_display()) if b))

  @permalink
  def get_absolute_url(self):
    """ Returns the URL to this city's detail view page. """
    if self.country == "us":
      return ('city_detail', None, {'country': slugify(self.country), 'state': slugify(self.state), 'city': slugify(self.city)})
    else:
      if self.province:
        return ('city_detail', None, {'country': slugify(self.country), 'state': slugify(self.province), 'city': slugify(self.city)})
      else:
        # Sort of ugly hack -- state detail view will check for cites without a state or province and
        # redirect them to the city detail view if appropriate.
        return ('state_detail', None, {'country': slugify(self.country), 'state': slugify(self.city)})

  @permalink
  def get_state_url(self):
    """ Returns the URL to the state detail view for the state or province of this city. """
    if self.country == "us":
      return ('state_detail', None, {'country': slugify(self.country), 'state': slugify(self.state)})
    else:
      return ('state_detail', None, {'country': slugify(self.country), 'state': slugify(self.province)})

  @permalink
  def get_country_url(self):
    """ Returns the URL to the city detail view for the country of this city. """
    return ('country_detail', None, {'country': slugify(self.country)})
  
  def location(self):
    """ Returns the GeolocatedItem object associated with this city. """
    try:
      return GeolocatedItem.objects.get(content_type=ContentType.objects.get_for_model(City), object_id=self.id)
    except:
      return None
  
  def aggregator_items(self):
    """ Returns a list of aggregator ContentItem objects which are geolocated in this city. """
    from savoy.contrib.aggregator.models import ContentItem
    return ContentItem.objects.filter(geolocated_item__city=self)
  
  def items(self):
    """ Returns a heterogeneous list of objects which are geolocated in this city. """
    from savoy.utils.date_sort import sort_items_by_date
    object_list = [ item.content_object for item in GeolocatedItem.objects.filter(city=self) if item.content_object ]
    return sort_items_by_date(object_list, recent_first=True)

  def item_count(self):
    """ Returns an integer representing the number of objects which are geolocated in this city. """
    return GeolocatedItem.objects.filter(city=self).count()

  def save(self, force_insert=False, force_update=False):
    """ Saves the city, and then creates or updates the GeolocatedItem object associated with it. """
    if self.province:
      self.slug = slugify(self.city + " " + self.province + " " + self.country)
    else:
      self.slug = slugify(self.city + " " + self.state + " " + self.country)
    super(City, self).save(force_insert=force_insert, force_update=force_update)
    GeolocatedItem.objects.create_or_update(self, address=self.full_name_ascii(), city=self)

  class Meta:
      verbose_name_plural = 'cities'
      unique_together = (('city', 'state', 'province', 'country'),)


class Neighborhood(models.Model):
  """ A distinct area within a city. """
  city        = models.ForeignKey(City, help_text="Select the city this neighborhood is in.", related_name="neighborhoods")
  name        = models.CharField(max_length=200, help_text='Enter the name of the neighborhood.')
  slug        = models.SlugField(help_text="The slug is a URL-friendly version of the name. It is auto-populated.")

  def __unicode__(self):
    return self.name
  
  def full_name(self):
    """ Returns the full name of the neighborhood in Neighborhood, City, State, Country format."""
    return ", ".join(b for b in (self.name, self.city.full_name()) if b)
  
  def places(self):
    """ Returns a list of Place objects representing places in this Neighborhood. """
    return [ item.content_object for item in GeolocatedItem.objects.filter(neighborhood=self, content_type=ContentType.objects.get_for_model(Place)) if item.content_object ]
  
  @permalink
  def get_absolute_url(self):
    """ Returns the URL to the detail page for this Neighborhood. """
    if self.city.country == "us":
      return ('neighborhood_detail', None, {'country': slugify(self.city.country), 'state': slugify(self.city.state), 'city': slugify(self.city.city), 'neighborhood_slug': self.slug})
    else:
      if self.city.province:
        return ('neighborhood_detail', None, {'country': slugify(self.city.country), 'state': slugify(self.city.province), 'city': slugify(self.city.city), 'neighborhood_slug': self.slug})
    return

  def aggregator_items(self):
    """ Returns aggregator ContentItem objects geolocated in this Neighborhood. """
    from savoy.contrib.aggregator.models import ContentItem
    return ContentItem.objects.filter(geolocated_item__neighborhood=self)
  
  def items(self):
    """ Returns a heterogenous list of objects geolocated in this Neighborhood. """
    from savoy.utils.date_sort import sort_items_by_date
    object_list = [ item.content_object for item in GeolocatedItem.objects.filter(neighborhood=self) if item.content_object ]
    return sort_items_by_date(object_list, recent_first=True)
    
  class Meta:
    unique_together = (("city", "name"),)
    
    
class PlaceType(models.Model):
  name        = models.CharField(max_length=50, unique=True, help_text="Type of place, i.e. 'Restaurant,' Park,' 'Coffee Shop,', etc.")
  plural_name = models.CharField(max_length=50, help_text="Plural name of the place type, i.e. 'Restaurants', 'Parks', etc.")
  slug        = models.SlugField('slug (plural)', unique=True)

  def __unicode__(self):
      return self.name

  class Meta:
      ordering = ('name',)


class Place(models.Model):
  ACCESS_CHOICES = (
      (0, 'Inaccessible'),
      (1, 'ADA-compliant'),
      (2, 'Very accommodating'),
      (3, 'Unknown'),
  )
  pre_name        = models.CharField(max_length=10, blank=True, help_text="Enter and prefixes, such as 'The', 'A', 'An,' etc.")
  name            = models.CharField(max_length=100, help_text="Enter the name of the place, i.e. 'Starbucks,' or 'My house'.")
  slug            = models.SlugField(unique=True, help_text="The slug is a URL-friendly version of the name. It is auto-populated.")
  nickname        = models.CharField(max_length=30, blank=True, help_text="If the place has a nickname, enter it here.")
  place_types     = models.ManyToManyField(PlaceType, verbose_name='types', blank=True, null=True, help_text="Select or add the types of places that define this location.")
  address1        = models.CharField('Address Line 1', max_length=100, blank=True)
  address2        = models.CharField('Address Line 2', max_length=50, blank=True)
  address_hint    = models.CharField(max_length=100, blank=True, help_text="Extra address info, like '8th and Western St.,' or 'Next to Starbucks'.")
  neighborhood    = models.ForeignKey(Neighborhood, blank=True, null=True, help_text="Select or add the neighborhood where this place is located.")
  city            = models.ForeignKey(City, blank=True, null=True, help_text="If no neighborhood is selected, select or add the city where this place is located.")
  zip_code        = models.CharField(max_length=5, blank=True, help_text="Enter the zip or postal code where this place is located.")
  phone1          = PhoneNumberField('Phone Number 1', blank=True, help_text="If the place has a phone number, enter it here.")
  phone2          = PhoneNumberField('Phone Number 2', blank=True, help_text="Optionally, enter a secondary phone number here.")
  fax             = PhoneNumberField(blank=True, help_text="If the place has a fax number, enter it here.")
  website         = models.URLField('Web site', blank=True, help_text="If the place has a phone number, enter its URL here.")
  email           = models.EmailField('E-mail', blank=True, help_text="If the place has an e-mail address, enter it here.")
  description     = models.TextField(blank=True, help_text="Enter a description of the place.")
  date_created    = models.DateTimeField(default=datetime.datetime.now, editable=False)
  is_public       = models.NullBooleanField(help_text="If this is a public place, select this box.")
  is_defunct      = models.NullBooleanField(help_text="If this place no longer exists, select this box.")
  is_outdoors     = models.NullBooleanField(help_text="If this place is outdoors, select this box.")
  accessibility   = models.PositiveSmallIntegerField(choices=ACCESS_CHOICES, default=3)
  tags            = TagField()

  def __unicode__(self):
    return self.name
      
  @permalink
  def get_absolute_url(self):
    """ Returns the URL to this place's detail page. """
    if self.city.country == "us":
      return ('place_detail', None, {'country': slugify(self.city.country), 'state': slugify(self.city.state), 'city': slugify(self.city.city), 'place_slug': self.slug})
    else:
      if self.city.province:
        return ('place_detail', None, {'country': slugify(self.city.country), 'state': slugify(self.city.province), 'city': slugify(self.city.city), 'place_slug': self.slug})
    return

  def location(self):
    """ Returns the geolocated item associated with this Place, if it exists. """
    try:
      return GeolocatedItem.objects.filter(content_type=ContentType.objects.get_for_model(Place), object_id=self.id)[0]
    except:
      return None

  def aggregator_items(self, radius_miles=.1):
    """ 
    Returns a list of aggregator ContentItem objects located within a given radius (defaults to .1 miles) of this place.
    Note that this is not a 100% accurate representation of items geolocated to this place, but it's the best we can
    do while maintaining solid performance.
    """
    if self.location():
      return self.location().get_aggregator_items_within_radius(radius_miles=radius_miles)
    else:
      return []

  def items(self, radius_miles=.1):
    """ 
    Returns a heterogenous list of objects located within a given radius (defaults to .1 miles) of this place.
    Note that this is not a 100% accurate representation of items geolocated to this place, but it's the best we can
    do while maintaining solid performance.
    """
    from savoy.utils.date_sort import sort_items_by_date
    object_list = [ item.content_object for item in self.location().get_geolocated_items_within_radius(radius_miles=radius_miles) if item.content_object ]
    return sort_items_by_date(object_list, recent_first=True)

  def display_name(self):
    """ Returns a display name for this Place, prepending the pre-name to the name. """
    return " ".join(b for b in (self.pre_name, self.name) if b)

  def full_name(self):
    """ Returns a full name for this Place, prepending the pre-name to the name and appending the city and zip code. """
    return ", ".join(b for b in (self.display_name, self.city.full_name(), self.zip_code) if b)

  def address(self):
    """ Returns the full address for this Place. """
    return ", ".join(b for b in (self.address1, self.address2, self.city.full_name(), self.zip_code) if b)

  def geolocation_address(self):
    """ Returns a full address for this Place in a format that seems to make geocoders happy. """
    if self.city.country == "us":
      return " ".join(b for b in (self.address1, self.address2, self.city.city, self.city.state, self.zip_code, self.city.country) if b)
    else:
      return " ".join(b for b in (self.address1, self.address2, self.city.city, self.zip_code, self.city.country) if b)

  def save(self, force_insert=False, force_update=False):
    """ 
    If a city hasn't been entered but a neighborhood has, assumes the city is the city associated with the neighborhood.
    Saves the Place, and then creates or updates the GeolocatedItem object for it.
    """
    if not self.city:
      if self.neighborhood:
        self.city = self.neighborhood.city
    super(Place, self).save(force_insert=force_insert, force_update=force_update)
    GeolocatedItem.objects.create_or_update(self, address=self.geolocation_address())

  class Meta:
      ordering = ('name',)


class UpcomingVenue(models.Model):
  place = models.ForeignKey(Place)
  upcoming_venue_id = models.IntegerField()
  user_id = models.IntegerField(blank=True, null=True)
  name = models.CharField(blank=True, max_length=200)
  url = models.URLField(blank=True, verify_exists=True)
  private = models.BooleanField(default=False)

  def __unicode__(self):
    return self.name



signals.post_delete.connect(GeolocatedItem.objects.remove_orphans, sender=City)
signals.post_delete.connect(GeolocatedItem.objects.remove_orphans, sender=Place)