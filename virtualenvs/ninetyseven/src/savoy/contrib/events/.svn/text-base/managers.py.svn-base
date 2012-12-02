from django.db import models

class UpcomingEventManager(models.Manager):
  """
  Custom manager for Events which only returns those which are from upcoming.yahoo.com.
  """
  def get_query_set(self):
    return super(UpcomingEventManager, self).get_query_set().filter(upcomingevent__isnull=False)

class UpcomingAttendEventManager(models.Manager):
  """
  Custom manager for Events which only returns those which are from upcoming.yahoo.com and have a status of "attend".
  """
  def get_query_set(self):
    return super(UpcomingAttendEventManager, self).get_query_set().filter(upcomingevent__isnull=False).filter(upcomingevent__status='attend')

class UpcomingWatchEventManager(models.Manager):
  """
  Custom manager for Events which only returns those which are from upcoming.yahoo.com and have a status of "attend".
  """
  def get_query_set(self):
    return super(UpcomingWatchEventManager, self).get_query_set().filter(upcomingevent__isnull=False).filter(upcomingevent__status='watch')
