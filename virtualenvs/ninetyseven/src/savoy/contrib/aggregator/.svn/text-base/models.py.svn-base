from django.db import models
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from tagging.fields import TagField

from savoy.contrib.aggregator.managers import *
from savoy.core.geo.models import GeolocatedItem

class ContentItem(models.Model):
  content_type        = models.ForeignKey(ContentType)
  object_id           = models.PositiveIntegerField()
  content_object      = GenericForeignKey()
  timestamp           = models.DateTimeField()
  geolocated_item     = models.ForeignKey(GeolocatedItem, blank=True, null=True)
  objects             = ContentItemManager()
  
  def __unicode__(self):
    return "%s: %s" % (self.content_type.model_class().__name__, unicode(self.content_object))
  
  def get_absolute_url(self):
    """ Call the get_absolute_url() method of this ContentItem's content object. """
    try:
      return self.content_object.get_absolute_url()
    except:
      return ""
  
  def _get_geo(self):
    try:
      geo = GeolocatedItem.objects.get(content_type=self.content_type, object_id=self.object_id)
    except:
      geo = None
    return geo
  
  def save(self, force_insert=False, force_update=False):
    self.geolocated_item = self._get_geo()
    super(ContentItem, self).save(force_insert=force_insert, force_update=force_update)
    
  class Meta:
    ordering          = ['-timestamp']
    unique_together   = [('content_type', 'object_id')]
    get_latest_by     = 'timestamp'