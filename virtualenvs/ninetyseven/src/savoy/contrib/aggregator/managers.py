import datetime

from django.conf import settings
from django.db import models
from django.db.models import signals
from django.contrib.contenttypes.models import ContentType

class ContentItemManager(models.Manager):
    
    def __init__(self):
      super(models.Manager, self).__init__()
      self._set_creation_counter()
      self.model = None
      self._inherited = False 
      self.models_by_name = {}
        
    def remove_orphans(self, instance, **kwargs):
      """
      When an item is deleted, first delete any ContentItem object that has been created
      on its behalf.
      """
      from savoy.contrib.aggregator.models import ContentItem
      try:
        instance_content_type = ContentType.objects.get_for_model(instance)
        content_item = ContentItem.objects.get(content_type=instance_content_type, object_id=instance.id)
        content_item.delete()
      except ContentItem.DoesNotExist:
        return
    
    def create_or_update(self, instance, timestamp=None, **kwargs):
        """
        Create or update a ContentItem from some instance.
        """
        from savoy.contrib.aggregator.models import ContentItem
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
        
        # Look at the AGGREGATOR_MODELS list in settings.py. It identifies which models
        # should be included in the aggregator, as well as what date field and manager
        # we should use for each one.
        for item in settings.AGGREGATOR_MODELS:
          this_app_label        = item['model'].split('.')[0]
          this_model_label      = item['model'].split('.')[1]
          this_content_type     = ContentType.objects.get(app_label=this_app_label, model=this_model_label)
          this_model            = this_content_type.model_class()
          
          if this_content_type == instance_content_type:
            try:
              manager         = item['manager']
            except:
              manager         = 'objects'
            try:
              timestamp_field = item['date_field']
            except:
              timestamp_field = 'date_published'
        
        # Make sure the item "should" be registered. This is based on the manager argument.
        # If InstanceModel.manager.all() includes this item, then it should be registered.
        # Otherwise, just return and don't add a ContentItem for this object.
        # If we find that it should NOT be registered, check to make sure we haven't already
        # registered this object in the past. If so, delete it.
        try:
            instance_exists = getattr(instance_model, manager).get(pk=instance.id)
        except instance_model.DoesNotExist:
            try:
              orphaned_content_item = ContentItem.objects.get(content_type=instance_content_type, object_id=instance._get_pk_val(),)
              orphaned_content_item.delete()
              return
            except:
              return
        
        # Pull the timestamp from the instance, using the timestamp_field argument.
        if hasattr(instance, timestamp_field):
            timestamp = getattr(instance, timestamp_field)
        
        # Create the ContentItem object.
        instance_content_type = ContentType.objects.get_for_model(instance)
        content_item, created = self.get_or_create(
            content_type = instance_content_type, 
            object_id = instance._get_pk_val(),
            defaults = dict(
              timestamp = timestamp,
            )
        )
        content_item.timestamp = timestamp
        # Save and return the item.
        content_item.save()
        return content_item
        
    def follow_model(self, model):
        """
        Follow a particular model class, updating associated ContentItems automatically.
        """
        self.models_by_name[model.__name__.lower()] = model
        signals.post_save.connect(self.create_or_update, sender=model)
        signals.post_delete.connect(self.remove_orphans, sender=model)
        
    def get_for_model(self, model):
        """
        Return a QuerySet of only items of a certain type.
        """
        return self.filter(content_type=ContentType.objects.get_for_model(model))
        
    def get_last_update_of_model(self, model, **kwargs):
        """
        Return the last time a given model's items were updated. Returns the
        epoch if the items were never updated.
        """
        qs = self.get_for_model(model)
        if kwargs:
            qs = qs.filter(**kwargs)
        try:
            return qs.order_by('-timestamp')[0].timestamp
        except IndexError:
            return datetime.datetime.fromtimestamp(0)