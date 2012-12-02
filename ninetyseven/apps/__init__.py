from django.db import models
from django.contrib.auth.models import User

from savoy.core.fields import CreationDateTimeField, ModificationDateTimeField

class BaseModel(models.Model):
  """
  Base class for models.
  
  """
  created_by    = models.ForeignKey(User, null=True, blank=True, related_name="%(class)s_created" )
  updated_by    = models.ForeignKey(User, null=True, blank=True, editable=False, related_name="%(class)s_updated")
  date_created  = CreationDateTimeField()
  date_updated  = ModificationDateTimeField()
  
  class Meta:
    abstract = True