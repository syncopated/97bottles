import datetime

from django.db import models

class CreationDateTimeField(models.DateTimeField):
  """
  By default, sets editable=False, blank=True, default=datetime.now
  """
  
  def __init__(self, *args, **kwargs):
      kwargs.setdefault('editable', False)
      kwargs.setdefault('blank', True)
      kwargs.setdefault('default', datetime.datetime.now)
      models.DateTimeField.__init__(self, *args, **kwargs)
  
  def get_internal_type(self):
      return "DateTimeField"

class ModificationDateTimeField(CreationDateTimeField):
    """ 
    By default, sets editable=False, blank=True, default=datetime.now
    Sets value to datetime.now() on each save of the model.
    """
    
    def pre_save(self, model, add):
        value = datetime.datetime.now()
        setattr(model, self.attname, value)
        return value
    
    def get_internal_type(self):
        return "DateTimeField"