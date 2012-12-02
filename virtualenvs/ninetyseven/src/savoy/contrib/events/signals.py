import datetime

from dateutil.rrule import *
from django.conf import settings

def update_event_times(sender, instance, signal, **kwargs):
  """Creates and updates EventTime objects for a given Event object."""
  event = instance.event
  
  from savoy.contrib.events.models import EventTime
  eventtimes = EventTime.objects.filter(event=event)
  
  # First, delete any event times that exist (clean slate).
  #for eventtime in eventtimes:
  #  eventtime.delete()

  # Create EventTime objects for any AllDayEventTimes
  for eventtime in event.all_day_eventtimes.all():
    start_time = datetime.datetime(year=eventtime.start_date.year, month=eventtime.start_date.month, day=eventtime.start_date.day, hour=0, minute=0, second=0)
    if eventtime.end_date:
      end_time = datetime.datetime(year=eventtime.end_date.year, month=eventtime.end_date.month, day=eventtime.end_date.day, hour=23, minute=59, second=59)
    else:
      end_time = datetime.datetime(year=eventtime.start_date.year, month=eventtime.start_date.month, day=eventtime.start_date.day, hour=23, minute=59, second=59)
    EventTime.objects.get_or_create(event=eventtime.event, start_time=start_time, end_time=end_time)

  # Create EventTime objects for any MonthlyEventTimes
  for eventtime in event.monthly_eventtimes.all():
    
    if eventtime.day_of_week == 1:
      weekday = SU
    if eventtime.day_of_week == 2:
      weekday = MO
    if eventtime.day_of_week == 3:
      weekday = TU
    if eventtime.day_of_week == 4:
      weekday = WE
    if eventtime.day_of_week == 5:
      weekday = TH
    if eventtime.day_of_week == 6:
      weekday = FR
    if eventtime.day_of_week == 7:
      weekday = SA
                  
    start_date = datetime.datetime(year=eventtime.start_date.year, month=eventtime.start_date.month, day=eventtime.start_date.day, hour=eventtime.start_time.hour, minute=eventtime.start_time.minute, second=eventtime.start_time.second)
    if eventtime.end_date:
      if eventtime.end_time:
        end_date = datetime.datetime(year=eventtime.end_date.year, month=eventtime.end_date.month, day=eventtime.end_date.day, hour=eventtime.end_time.hour, minute=eventtime.end_time.minute, second=eventtime.end_time.second)
      else:
        end_date = eventtime.end_date
      recurrences = list(rrule(MONTHLY, byweekday=weekday(int(eventtime.week_of_month)), dtstart=start_date, until=end_date))
    else:
      recurrences = list(rrule(MONTHLY, byweekday=weekday(int(eventtime.week_of_month)), dtstart=start_date, count=settings.RECURRING_EVENT_TIME_LIMIT))
    for recurrence in recurrences:
      end_time = datetime.datetime(year=recurrence.year, month=recurrence.month, day=recurrence.day, hour=eventtime.end_time.hour, minute=eventtime.end_time.minute, second=eventtime.end_time.second)
      EventTime.objects.get_or_create(event=eventtime.event, start_time=recurrence, end_time=end_time)

  # Create EventTime objects for any WeeklyEventTimes
  for eventtime in event.weekly_eventtimes.all():
    
    if eventtime.day_of_week == 1:
      weekday = SU
    if eventtime.day_of_week == 2:
      weekday = MO
    if eventtime.day_of_week == 3:
      weekday = TU
    if eventtime.day_of_week == 4:
      weekday = WE
    if eventtime.day_of_week == 5:
      weekday = TH
    if eventtime.day_of_week == 6:
      weekday = FR
    if eventtime.day_of_week == 7:
      weekday = SA
  
    start_date = datetime.datetime(year=eventtime.start_date.year, month=eventtime.start_date.month, day=eventtime.start_date.day, hour=eventtime.start_time.hour, minute=eventtime.start_time.minute, second=eventtime.start_time.second)
    if eventtime.end_date:
      if eventtime.end_time:
        end_date = datetime.datetime(year=eventtime.end_date.year, month=eventtime.end_date.month, day=eventtime.end_date.day, hour=eventtime.end_time.hour, minute=eventtime.end_time.minute, second=eventtime.end_time.second)
      else:
        end_date = eventtime.end_date
      recurrences = list(rrule(WEEKLY, wkst=SU, byweekday=weekday, dtstart=start_date, until=end_date))
    else:
      recurrences = list(rrule(WEEKLY, wkst=SU, byweekday=weekday, dtstart=start_date, count=settings.RECURRING_EVENT_TIME_LIMIT/12*52))
    for recurrence in recurrences:
      end_time = datetime.datetime(year=recurrence.year, month=recurrence.month, day=recurrence.day, hour=eventtime.end_time.hour, minute=eventtime.end_time.minute, second=eventtime.end_time.second)
      EventTime.objects.get_or_create(event=eventtime.event, start_time=recurrence, end_time=end_time)
    
  
  # Create EventTime objects for any OneOffEventTimes
  for eventtime in event.one_off_eventtimes.all():
    if eventtime.end_time:
      EventTime.objects.get_or_create(event=eventtime.event, start_time=eventtime.start_time, end_time=eventtime.end_time)
    else:
      EventTime.objects.get_or_create(event=eventtime.event, start_time=eventtime.start_time)