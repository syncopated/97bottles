from django.db import models
from django.db.models import signals
from django.contrib.contenttypes.models import ContentType

from savoy.core.geo.models import *
from savoy.core.geo.utils.misc import *


class GeolocatedItemManager(models.Manager):
    def remove_orphans(self, instance, **kwargs):
      """
      When an item is deleted, first delete any GeolocatedItem object that has been created
      on its behalf.
      """
      from savoy.core.geo.models import GeolocatedItem
      try:
        instance_content_type = ContentType.objects.get_for_model(instance)
        geolocated_item = GeolocatedItem.objects.get(content_type=instance_content_type, object_id=instance.id)
        geolocated_item.delete()
      except GeolocatedItem.DoesNotExist:
        return
    
    def create_or_update(self, instance, location=None, address=None, city=None, neighborhood=None, **kwargs):
      """
      Create or update a GeolocatedItem from some instance. Instance must provide
      either (latitude,longitude) or an address for geocoding.
      """
      from savoy.core.geo.models import GeolocatedItem
      # If the instance hasn't already been saved, save it first.
      if instance._get_pk_val() is None:
        try:
          signals.post_save.disconnect(self.create_or_update, sender=type(instance))
        except:
          reconnect = False
        else:
          reconnect = True
        instance.save()
        if reconnect:
          signals.post_save.connect(self.create_or_update, sender=type(instance))

      # Find this object's content type and model class.
      instance_content_type = ContentType.objects.get_for_model(instance)
      instance_model        = instance_content_type.model_class()
      
      # If we got an address, we need to geocode it.
      if address:
        location = get_location_from_address(address)
      
      # We should now have a location tuple (either passed in or geolocated
      # from the passed in address). Unpack it.
      if location:
        latitude, longitude = location
      
        # Determine the city and neighborhood for this geolocated item.
        if not city:
          city = get_city_from_flickr(latitude, longitude)
        if not neighborhood:
          try:
            neighborhood = get_neighborhood_from_urban_mapping(latitude, longitude, city)
          except:
            neighborhood = None
      
        # Get or create the GeolocatedItem object.
        geolocated_item, created = self.get_or_create(
          content_type = instance_content_type, 
          object_id = instance._get_pk_val(),
          defaults = dict(
            city = city,
            neighborhood = neighborhood,
            latitude = str(latitude),
            longitude = str(longitude),
          )
        )

        # If this is not a new GeolocatedItem object, update it with current data.
        if not created:
          geolocated_item.latitude = str(latitude)
          geolocated_item.longitude = str(longitude)
          geolocated_item.city = city
          geolocated_item.neighborhood = neighborhood
      
        # Save and return the item.
        geolocated_item.save()
        return geolocated_item
      else:
        return
        
    def get_for_model(self, model):
      """
      Return a QuerySet of only items of a certain type.
      """
      return self.filter(content_type=ContentType.objects.get_for_model(model))