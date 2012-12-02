import datetime
from decimal import Decimal

from django import template
from django.template import Library, resolve_variable
from django.contrib.contenttypes.models import ContentType

from savoy.core.geo.models import *

register = Library()

class GetPhotosNearPlaceNode(template.Node):
    def __init__(self, place, varname, radius=25):
      self.place, self.varname, self.radius = place, varname, radius

    def render(self, context):
      from savoy.core.media.models import Photo
      from django.core.cache import cache
      
      self.place = resolve_variable(self.place, context)
      
      # First, check and see if we have this data in the cache. If so, return it.
      cache_key = "place-photos-" + str(self.radius) + "-" + str(self.place.id)
      
      if type(cache.get(cache_key)) == type([]):
        context[self.varname] = cache.get(cache_key)
        return ''
      
      # If not, look it up.
      else:
        if self.place.location:
          radius = float(self.radius)
          photo_content_type = ContentType.objects.get_for_model(Photo)
          photos_within_radius = self.place.location.get_geolocated_items_within_radius(radius).filter(content_type=photo_content_type)
          photo_list = []
        
          # This code ensures each photo's closet place is the place in question. In effect,
          # it ties every photo to exactly one place. After thinking about it, I decided I didn't want
          # this. But, I'm keeping it around, in in case I change my mind.
        
          # for geo in photos_within_radius:
          #   if geo.content_object is not None:
          #     if geo.get_closest_place()['place'] == self.place:
          #         photo_list.append(geo.content_object)

          # This code, on the other hands, returns all photos in the radius, regardless of whether or
          # not this place is the closest one to the photo.
        
          for geo in photos_within_radius:
            if geo.content_object is not None:
                photo_list.append(geo.content_object)

          # Save the data to the cache and then return it.
          cache.set(cache_key,photo_list,28800)
          context[self.varname] = photo_list
      
      return ''

@register.tag
def get_photos_near_place(parser, token):
    """
    Retrieves photos taken near this place. Radius defaults to 25 miles if it is not given.

    Syntax::

        {% get_photos_near_place [place] as [varname] (with mile radius [miles]) %}

    Example::

        {% get_photos_near_place place as place_photos with mile radius 1.5 %}

    """
    bits = token.contents.split()
    try:
      return GetPhotosNearPlaceNode(bits[1], bits[3], bits[7])
    except:
      return GetPhotosNearPlaceNode(bits[1], bits[3])