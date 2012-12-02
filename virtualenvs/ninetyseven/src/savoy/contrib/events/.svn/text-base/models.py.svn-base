import datetime

from django.db import models
from django.db.models import signals
from django.db.models import permalink
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from django.conf import settings
from tagging.fields import TagField

from savoy.core.geo.models import Place, GeolocatedItem
from savoy.core.people.models import Person
from savoy.core.organizations.models import Organization
from savoy.core.constants import DAY_OF_WEEK_CHOICES, WEEK_OF_MONTH_CHOICES
from savoy.contrib.events.signals import update_event_times
from savoy.contrib.events.managers import *


class Event(models.Model):
  """An event is an occurrence at a place."""
  title                       = models.CharField(max_length=250, help_text="Enter the title of this event.")
  slug                        = models.SlugField(max_length=200, unique_for_date="date_created", help_text='The slug is a URL-friendly version of the title. It is auto-populated.')
  short_description           = models.CharField(blank=True, max_length=200, help_text="Add a one-line description for the event.")
  description                 = models.TextField(blank=True, help_text='Add a full description for the event.')
  tags                        = TagField(help_text="Add tags for this event.")
  places                      = models.ManyToManyField(Place, blank=True, help_text="Add or select locations where this events will take place.", related_name="event_places")
  organizers                  = models.ManyToManyField(Organization, blank=True, help_text="Add or select the organizations holding this event.", related_name="event_organizations")
  sponsors                    = models.ManyToManyField(Organization, blank=True, help_text="Add or select the organizations sponsoring this event.", related_name="event_sponsors")
  individual_organizers       = models.ManyToManyField(Person, blank=True, help_text="Add or select the people holding this event.", related_name="event_individual_organizers")
  individual_sponsors         = models.ManyToManyField(Person, blank=True, help_text="Add or select the people sponsoring this event.", related_name="event_individual_sponsors")
  added_by                    = models.ForeignKey(Person, blank=True, null=True, help_text='Select the person adding this event.')
  date_published              = models.DateTimeField(default=datetime.datetime.now, help_text="Enter the date this event should begin displaying on the site.")
  date_created                = models.DateTimeField(default=datetime.datetime.now, editable=False)
  cost_high                   = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Enter the maximum cost.")
  cost_low                    = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Enter the minimum cost.")
  event_url                   = models.URLField(blank=True, verify_exists=True, help_text="Enter the URL of the website for this event.")
  ticket_url                  = models.URLField(blank=True, verify_exists=True, help_text="Enter the URL of the website to purchase tickets from.")
  objects                     = models.Manager()
  attend_events               = UpcomingAttendEventManager()
  watch_events                = UpcomingWatchEventManager()
    
  def __unicode__(self):
    return force_unicode(self.title)
  
  @permalink
  def get_absolute_url(self):
    """ Returns the URL to this event's detail page. """
    return ('event_detail', None, {'object_id': self.id} )
  
  @property
  def start_time(self):
    """ 
    Returns the start time from the first EventTime for this event.
    Note that this is not ideal, but it's the best I could come up with.
    """
    return self.get_first_eventtime().start_time
  
  def upcoming_event(self):
    """ If this event was imported from Upcoming, returns the associated UpcomingEvent object. """
    try:
      return UpcomingEvent.objects.get(event=self)
    except:
      return None
  
  def is_upcoming_event(self):
    """ Returns True if this event was imported from Upcoming. """
    if self.upcoming_event():
      return True
    else:
      return False
  
  def get_next_eventtime(self):
    """ Returns the next EventTime object for this event. """
    try:
      now = datetime.datetime.now()
      eventtimes = EventTime.objects.filter(event=self, start_time__gte=now).order_by('start_time')
      return eventtimes[0]
    except:
      return None
      
  def get_first_eventtime(self):
    """ Returns the first (oldest) EventTime object for this event. """
    try:
      eventtimes = EventTime.objects.filter(event=self).order_by('start_time')
      return eventtimes[0]
    except:
      return None
  
  def save(self, force_insert=False, force_update=False):
    """ 
    Saves the Event. If the Event has places, geolocates it to the first Place in the list.
    This may not be ideal, but our GeolocatedItem system currently only allows an object to be
    geolocated to exactly one place.
    """
    super(Event, self).save(force_insert=force_insert, force_update=force_update)
    if self.places.all():
      GeolocatedItem.objects.create_or_update(self, address=self.places.all()[0].geolocation_address())
  
  class Meta:
    ordering = ['title',]


class UpcomingEvent(models.Model):
  """An UpcomingEvent object contains a relationship to an event and upcoming.yahoo.com metadata about that event. """
  event                     = models.ForeignKey(Event)
  upcoming_event_id         = models.IntegerField()
  category_id               = models.IntegerField(blank=True, null=True)
  user_id                   = models.IntegerField(blank=True, null=True)
  metro_id                  = models.IntegerField(blank=True, null=True)
  venue_id                  = models.IntegerField(blank=True, null=True)
  date_posted               = models.DateField(blank=True, null=True)
  status                    = models.CharField(blank=True, max_length=100)
  
  property
  def url(self):
    """ Returns the URL to this event on Upcoming. """
    return "http://upcoming.yahoo.com/event/" + str(self.upcoming_event_id) + "/"
  
  def __unicode__(self):
    return self.event.title


class OneOffEventTime(models.Model):
  """One off event times are occurrences of an event at non-regular times. i.e. March 2nd, 8:00pm."""
  event                       = models.ForeignKey(Event, help_text="Add or select the event this time is associated with.", related_name="one_off_eventtimes")
  start_time                  = models.DateTimeField(help_text="Enter the start date and time for this event.")
  end_time                    = models.DateTimeField(blank=True, null=True, help_text="Enter the end date and time for this event.")
  is_from_upcoming            = models.BooleanField(default=False, editable=False)

  def __unicode__(self):
    return force_unicode(self.event) + ', ' + force_unicode(self.start_time)


class AllDayEventTime(models.Model):
  """All day event times are occurrences of an event on a date, but without a specific time. i.e. March 2nd."""
  event                       = models.ForeignKey(Event, help_text="Add or select the event this time is associated with.", related_name="all_day_eventtimes")
  start_date                  = models.DateField(help_text="Enter the start date for this event.")
  end_date                    = models.DateField(blank=True, null=True, help_text="Enter the end date for this event.")
  is_from_upcoming            = models.BooleanField(default=False, editable=False)

  def __unicode__(self):
    return str(self.event) + ', ' + str(self.start_date)


class WeeklyEventTime(models.Model):
  """Weekly event times are occurrences of an event on a specific day every week. i.e. Every Sunday at 8pm from now until the end of August, 2007."""
  event                       = models.ForeignKey(Event, help_text="Add or select the event this time is associated with.", related_name="weekly_eventtimes")
  day_of_week                 = models.IntegerField(choices=DAY_OF_WEEK_CHOICES, help_text="Select the day of week this event occurs on.")
  start_time                  = models.TimeField(help_text="Enter the start time for this recurring event.")
  end_time                    = models.TimeField(blank=True,null=True,  help_text="Enter the end time for this recurring event.")
  start_date                  = models.DateField(help_text="Enter the start date for this recurring event.")
  end_date                    = models.DateField(blank=True, null=True, help_text="Enter the end date for this recurring event.")
  is_from_upcoming            = models.BooleanField(default=False, editable=False)

  def __unicode__(self):
    return str(self.event) + ", every " + str(self.get_day_of_week_display()) + " at " + str(self.start_time)


class MonthlyEventTime(models.Model):
  """Monthly event times are occurrences of an event on a specific day every month. i.e. The first Friday of every month until November, 2009."""
  event                       = models.ForeignKey(Event, help_text="Add or select the event this time is associated with.", related_name="monthly_eventtimes")
  week_of_month               = models.CharField(max_length=2, choices=WEEK_OF_MONTH_CHOICES, help_text="Select the week of the month this event occurs on.")
  day_of_week                 = models.IntegerField(choices=DAY_OF_WEEK_CHOICES, help_text="Select the day of week this event occurs on.")
  start_time                  = models.TimeField(help_text="Enter the start time for this recurring event.")
  end_time                    = models.TimeField(blank=True, null=True, help_text="Enter the end time for this recurring event.")
  start_date                  = models.DateField(help_text="Enter the start date for this recurring event.")
  end_date                    = models.DateField(blank=True, null=True, help_text="Enter the end date for this recurring event.")
  is_from_upcoming            = models.BooleanField(default=False, editable=False)

  def __unicode__(self):
    return str(self.event) + ", the " + self.get_week_of_month_display() + " " + self.get_day_of_week_display() + " of the month at " + str(self.start_time)


class EventTime(models.Model):
  event                       = models.ForeignKey('Event')
  start_time                  = models.DateTimeField()
  end_time                    = models.DateTimeField(blank=True, null=True)
  
  def __unicode__(self):
    return force_unicode(str(self.event)) + " at " + force_unicode(str(self.start_time))

  @permalink
  def get_absolute_url(self):
    """ Returns the URL to the detail page for this EventTime. """
    return ('eventtime_detail', None, {
      'year':         self.start_time.strftime("%Y").lower(),
      'month':        self.start_time.strftime("%b").lower(),
      'day':          self.start_time.strftime("%d").lower(),
      'slug':         self.event.slug, 
      'eventtime_id': self.id,
    })
    
  def is_in_past(self):
    """ Returns True if this EventTime has already occurred. """
    now = datetime.datetime.now()
    if self.end_time:
      return self.end_time < now
    else:
      return self.start_time < now

  def date_published(self):
    """ Proxies to the associated Event object's date_published field. """
    return self.event.date_published
  
  def save(self, force_insert=False, force_update=False):
    """ 
    Saves the EventTime. If the Event has places, geolocates it to the first Place in the list.
    This may not be ideal, but our GeolocatedItem system currently only allows an object to be
    geolocated to exactly one place.
    """
    super(EventTime, self).save(force_insert=force_insert, force_update=force_update)
    if self.event.places.all():
      GeolocatedItem.objects.create_or_update(self, address=self.event.places.all()[0].geolocation_address())
  
  class Meta:
    ordering = ['-start_time', '-end_time']


# When an Event is added or updated, update the EventTimes for that Event.
signals.post_save.connect(update_event_times, sender=OneOffEventTime)
signals.post_save.connect(update_event_times, sender=AllDayEventTime)
signals.post_save.connect(update_event_times, sender=WeeklyEventTime)
signals.post_save.connect(update_event_times, sender=MonthlyEventTime)
signals.post_delete.connect(GeolocatedItem.objects.remove_orphans, sender=Event)
signals.post_delete.connect(GeolocatedItem.objects.remove_orphans, sender=EventTime)