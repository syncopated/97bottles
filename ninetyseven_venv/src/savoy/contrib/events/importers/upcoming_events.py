from savoy.utils.path import append_third_party_path
append_third_party_path()

import datetime
import time
from django.template.defaultfilters import slugify, upper
from upcoming_api import Upcoming
from tagging.models import Tag
from savoy.contrib.events.models import *
from savoy.core.geo.models import *
from django.conf import settings
from django.utils.encoding import force_unicode
from savoy.utils.slugs import get_unique_slug_value
from savoy.core.geo.utils.misc import get_city_from_flickr
from savoy.third_party.ascii_dammit import asciiDammit

upcoming = Upcoming(settings.UPCOMING_API_KEY)

def _create_or_update_oneoffeventtime(event, upcoming_event_info):
  """
  Adds a OneOffEventTime object for the related event.
  """
  # Create datetime objects for the appropriate start and end times and dates.
  if upcoming_event_info['start_time']:
    start_time = datetime.datetime(year=upcoming_event_info['start_date'].year, month=upcoming_event_info['start_date'].month, day=upcoming_event_info['start_date'].day, hour=upcoming_event_info['start_time'].hour, minute=upcoming_event_info['start_time'].minute, second=upcoming_event_info['start_time'].second)
  else:
    start_time = upcoming_event_info['start_date']
  if upcoming_event_info['end_date'] and upcoming_event_info['end_time']:
    end_time = datetime.datetime(year=upcoming_event_info['end_date'].year, month=upcoming_event_info['end_date'].month, day=upcoming_event_info['end_date'].day, hour=upcoming_event_info['end_time'].hour, minute=upcoming_event_info['end_time'].minute, second=upcoming_event_info['end_time'].second)
  elif upcoming_event_info['end_time']:
    end_time = datetime.datetime(year=upcoming_event_info['start_date'].year, month=upcoming_event_info['start_date'].month, day=upcoming_event_info['start_date'].day, hour=upcoming_event_info['end_time'].hour, minute=upcoming_event_info['end_time'].minute, second=upcoming_event_info['end_time'].second)
  else:
    end_time = upcoming_event_info['end_date']
  
  oneoffeventtime, created_oneoffeventtime = OneOffEventTime.objects.get_or_create(
    event=event, 
    is_from_upcoming=True,
    defaults = dict(
      start_time = start_time,
      end_time = end_time,
    ),
  )
  oneoffeventtime.save()
  return oneoffeventtime





def _create_or_update_alldayeventtime(event, upcoming_event_info):
  """
  Adds an AddDayEventTime object for the related event.
  """
  alldayeventtime, created_alldayeventtime = AllDayEventTime.objects.get_or_create(
    event=event, 
    is_from_upcoming=True,
    defaults = dict(
      start_date          = upcoming_event_info['start_date'],
      end_date            = upcoming_event_info['end_date'],
    ),
  )
  alldayeventtime.save()
  return alldayeventtime


def _create_or_update_related_objects(event, upcoming_event_info, watchlist_event):
  # Create or update it's UpcomingEvent object.
  try:
    _create_or_update_upcomingevent_for_event(event, upcoming_event_info, watchlist_event)
  except:
    print "\tERROR: There was an error saving the UpcomingEvent object."

  # Create or update it's Place object. Pause a couple seconds first, so we don't
  # accidentially hit UrbanMapping's API limit.
  try:
    time.sleep(2)
    event_place = _create_or_update_place_for_event(event, upcoming_event_info)
    if event_place:
      event.places.add(event_place)
  except:
    print "\tERROR: There was an error saving the Place object."

  # Create or update the EventTime objects.
  try:
    today = datetime.date.today()
    if upcoming_event_info['start_time']:
      _create_or_update_oneoffeventtime(event, upcoming_event_info)
    else:
      _create_or_update_alldayeventtime(event, upcoming_event_info)
  except:
    raise
    print "\t ERROR: There was an error saving the EventTime objects."
  return
  
  

def _create_or_update_event(upcoming_id, watchlist_event):
  """
  Adds an Event object for the upcoming event.
  """
  try:
    upcoming_event_info = upcoming.event.getInfo(event_id=upcoming_id)[0]
  except:
    return "ERROR: There was an error retrieving event " + str(upcoming_id)

  try:
    # Look for an UpcomingEvent with this ID. If found, update the UpcomingEvent's related
    # event with any new title, description, or tags.
    print "Found event: " + upcoming_event_info['name']
    upcoming_event                = UpcomingEvent.objects.get(upcoming_event_id=upcoming_id)
    event                         = upcoming_event.event
    if event.get_first_eventtime():
      if not event.get_first_eventtime().is_in_past:
        event.title                   = force_unicode(upcoming_event_info['name'])
        event.description             = force_unicode(upcoming_event_info['description'])
        event.tags                    = force_unicode(" ".join(upcoming_event_info['tags'][0:15]))
        event.save()
        # If this is an event in the future, make sure it's related objects are all up to date.
        # If it's an event in the past, we don't really care.
        if event.get_first_eventtime():
          if not event.get_first_eventtime().is_in_past:
            _create_or_update_related_objects(event, upcoming_event_info, watchlist_event)

  except UpcomingEvent.DoesNotExist:
    # If we didn't find an UpcomingEvent with this ID, it's a new event. Create an event
    # with the appropriate info and call _create_or_update_upcomingevent_for_event to create
    # the associated UpcomingEvent.
    event = Event(
      title                     = force_unicode(upcoming_event_info['name']),
      description               = force_unicode(upcoming_event_info['description']),
      tags                      = force_unicode(" ".join(upcoming_event_info['tags'][0:15])),
      date_created              = datetime.datetime.now(),
      date_published            = datetime.datetime.now(),
      slug                      = get_unique_slug_value(Event, slugify(upcoming_event_info['name'])),
    )
    event.save()
    _create_or_update_related_objects(event, upcoming_event_info, watchlist_event)





def _delete_orphaned_upcoming_events(upcoming_event_ids):
  """
  Checks to see if there are events still in our database that are no longer on upcoming.org,
  and deletes any it finds.
  """
  for upcoming_event in UpcomingEvent.objects.all():
    if not upcoming_event.upcoming_event_id in upcoming_event_ids:
      print "Removing event " + upcoming_event.event.title
      one_off_event_times = OneOffEventTime.objects.filter(event=upcoming_event.event)
      for o in one_off_event_times:
        try:
          o.delete()
        except:
          pass
      all_day_event_times = AllDayEventTime.objects.filter(event=upcoming_event.event)
      for a in one_off_event_times:
        try:
          a.delete()
        except:
          pass
      event_times = EventTime.objects.filter(event=upcoming_event.event)
      for e in event_times:
        e.delete()
      upcoming_event.event.delete()
      upcoming_event.delete()
  return


def _create_or_update_upcomingevent_for_event(event, upcoming_event_info, watchlist_event):
  """
  Adds an UpcomingEvent object for the related event.
  """
  upcoming_event, created_upcoming_event = UpcomingEvent.objects.get_or_create(
    upcoming_event_id=upcoming_event_info['id'],
    defaults = dict(
      event        = event,
      category_id  = upcoming_event_info['category_id'],
      user_id      = upcoming_event_info['user_id'],
      metro_id     = upcoming_event_info['metro_id'],
      venue_id     = upcoming_event_info['venue_id'],
      date_posted  = upcoming_event_info['date_posted'],
    ),
  )

  if not created_upcoming_event:
    upcoming_event.category_id  = upcoming_event_info['category_id']
    upcoming_event.user_id      = upcoming_event_info['user_id']
    upcoming_event.metro_id     = upcoming_event_info['metro_id']
    upcoming_event.venue_id     = upcoming_event_info['venue_id']
    upcoming_event.date_posted  = upcoming_event_info['date_posted']
    
  try:
    upcoming_event.status       = watchlist_event['status']
  except:
    pass
    
  upcoming_event.save()




def _create_or_update_place_for_event(event, upcoming_event_info):
  """
  Adds a Place object and an UpcomingVenue object for the related venue.
  """
  try:
    upcoming_venue_info = upcoming.venue.getInfo(venue_id=upcoming_event_info['venue_id'])[0]
    upcoming_metro_info = upcoming.metro.getInfo(metro_id=upcoming_event_info['metro_id'])[0]
  except:
    print "\tERROR: There was an error retrieving the Upcoming venue or metro information for this event."
    return None
    
  upcoming_venue, created_upcoming_venue = UpcomingVenue.objects.get_or_create(
    upcoming_venue_id=upcoming_venue_info['id'],
  )
  if not created_upcoming_venue:
    place                 = upcoming_venue.place
    place.website         = upcoming_venue_info['url']
    place.description     = upcoming_venue_info['description']
    place.address1        = upcoming_venue_info['address']
    place.phone1          = upcoming_venue_info['phone']
  else:
    place = Place(
      name            = upcoming_venue_info['name'],
      slug            = get_unique_slug_value(Place, slugify(upcoming_venue_info['name']))[:30],
      website         = upcoming_venue_info['url'],
      description     = upcoming_venue_info['description'],
      address1        = upcoming_venue_info['address'],
      phone1          = upcoming_venue_info['phone'],
      phone2          = '',
      fax             = '',
    )
    if len(upcoming_venue_info['zip']) <= 5:
      place.zip_code = upcoming_venue_info['zip']

    # Get the city from flickr's API instead of using Upcoming's data, as Flickr's is MUCH more normalized.
    place.city = get_city_from_flickr(city_name=upcoming_venue_info['city'], state=upper(upcoming_metro_info['state_code']), country=upcoming_metro_info['country_code'])
    if place.city:
      print "\tFound city " + str(place.city) + " using Flickr's places API."
    else:
      # If flickr doesn't get us any data, we'll use Upcoming's (shitty) data.
      print "\t Couldn't find the city in Flickr's API; falling back to Upcoming's."
      city      = upcoming_venue_info['city'],
      state     = upper(upcoming_metro_info['state_code'])
      if len(upcoming_metro_info['country_code']) == 2:
        country = upcoming_metro_info['country_code']
      else:
        country = ''
      city, created_city = City.object.get_or_create(
        city      = city, 
        state     = state,
        country   = country,
        slug      = slugify(asciiDammit(city) + " " + asciiDammit(state) + " " + asciiDammit(country)),
      )
      if created_city:
        city.save()
    place.city = city
  
  place.save()

  upcoming_venue.place    = place
  upcoming_venue.user_id  = upcoming_venue_info['user_id']
  upcoming_venue.name     = upcoming_venue_info['name']
  upcoming_venue.url      = upcoming_venue_info['url']
  upcoming_venue.private  = upcoming_venue_info['private']
  upcoming_venue.save()

  return place





def update():
  upcoming_event_ids = []

  upcoming_user_id = upcoming.user.getInfoByUsername(username=settings.UPCOMING_USERNAME)[0]['id']
  watchlist = upcoming.user.getWatchlist(token=settings.UPCOMING_TOKEN, user_id=upcoming_user_id, show='all')

  print "Found " + str(len(watchlist)) + " Upcoming events to import...\n\n"

  for watchlist_event in watchlist:
    upcoming_id = watchlist_event['id']
    _create_or_update_event(upcoming_id, watchlist_event)
    upcoming_event_ids.append(upcoming_id)
  _delete_orphaned_upcoming_events(upcoming_event_ids)
  
  # except:
  #   try:
  #     event_list = []
  #     for tag in settings.UPCOMING_SEARCH_TAGS:
  #       events = upcoming.event.search(search_text=tag)
  #       for event in events:
  #         event_list.append(event)
  #         
  #     print "Found " + str(len(event_list)) + " Upcoming events to import...\n\n"
  #     
  #   except:
  #     print "No username or tag list was found in settings.py"
  #   
  #   for event in event_list:
  #     upcoming_id = event['id']
  #     _create_or_update_event(upcoming_id, event)
  #     upcoming_event_ids.append(upcoming_id)

if __name__ == '__main__':
    update()