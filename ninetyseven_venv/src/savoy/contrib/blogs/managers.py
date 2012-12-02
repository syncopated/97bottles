import datetime
from django.db import models

class ActiveBlogManager(models.Manager):
  """
  Custom manager for blogs which only returns blogs with status 'Active'.
  """
  def get_query_set(self):
    return super(ActiveBlogManager, self).get_query_set().filter(status__exact=1)

class FeaturedBlogManager(models.Manager):
  """
  Custom manager for blogs which only returns blogs marked as featured.
  """
  def get_query_set(self):
    return super(FeaturedBlogManager, self).get_query_set().filter(featured__exact=1)
    
    
class LiveEntryManager(models.Manager):
  """
  Custom manager for entries which only returns entries with status 'Live'.
  """
  def get_query_set(self):
    return super(LiveEntryManager, self).get_query_set().filter(status__exact=2, date_published__lte=datetime.datetime.now())


class FeaturedEntryManager(models.Manager):
  """
  Custom manager for entries which only returns entries marked as featured.
  """
  def get_query_set(self):
    return super(FeaturedEntryManager, self).get_query_set().filter(featured__exact=1)