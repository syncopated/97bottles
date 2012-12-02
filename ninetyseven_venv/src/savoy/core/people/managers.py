from django.db import models
from django.db.models import signals
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify

class PersonManager(models.Manager):
  def create_or_update(self, instance, **kwargs):
    """
    Create or update a Person from some User.
    """
    if instance.first_name and instance.last_name:
      slug = slugify(instance.first_name + ' ' + instance.last_name)
    else:
      slug = instance.username
      
    if instance.first_name:
      first_name = instance.first_name
    else:
      first_name = instance.username
      
    if instance.last_name:
      last_name = instance.last_name
    else:
      last_name = ""
    
    person, created = self.get_or_create(
      user = instance,
      defaults = dict(
        slug = slug,
        first_name = first_name,
        last_name = last_name,
      )
    )
    return person