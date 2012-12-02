import datetime

from django.db import models

class LivePageManager(models.Manager):
  """
  Custom manager for entries which only returns page with status 'Live' and that are past their pub_date.
  """
  def get_query_set(self):
      return super(LivePageManager, self).get_query_set().filter(status__exact=2, pub_date__lte=datetime.datetime.now())
