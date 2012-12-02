from django.db import models

class LiveBookmarkManager(models.Manager):
  """
  Custom manager for entries which only returns public, live bookmarks.
  """
  def get_query_set(self):
    return super(LiveBookmarkManager, self).get_query_set().filter(private=False)