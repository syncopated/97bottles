from django import template
from django.template import Library
from savoy.contrib.events.models import *
import datetime
from django.db.models import Q
from django.template import resolve_variable

register = Library()

class GetUpcomingEventtimesNode(template.Node):
    def __init__(self, status, num, varname):
      self.status, self.num, self.varname = status, num, varname

    def render(self, context):
      now = datetime.datetime.now()
      if self.status == 'all':
        context[self.varname] = EventTime.objects.filter(
          Q(event__upcomingevent__isnull=False),
          Q(start_time__gte=now) | (Q(end_time__gte=now) & Q(end_time__isnull=False)),
        ).order_by('start_time')[:self.num]
      else:
        status = str(self.status)      
        context[self.varname] = EventTime.objects.filter(
          Q(event__upcomingevent__status=status),
          Q(event__upcomingevent__isnull=False),
          Q(start_time__gte=now) | (Q(end_time__gte=now) & Q(end_time__isnull=False)),
        ).order_by('start_time')[:self.num]
        
      return ''

@register.tag
def get_upcoming_eventtimes(parser, token):
    """
    Retrieves a given number of upcoming EventTimes (events which start after the current date/time),
    sorted by start date.

    Syntax::

        {% get_upcoming_eventtimes [status(attend|watch|all)] [num] as [varname] %}

    Example::

        {% get_upcoming_eventtimes attend 5 as upcoming_eventtimes %}

    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise template.TemplateSyntaxError("'%s' tag takes four arguments" % bits[0])
    #if bits[1] != 'attend' or 'watch' or 'all':
    #    raise template.TemplateSyntaxError("first argument to '%s' tag must be 'attend', 'watch', or 'all'." % bits[0])
    if bits[3] != 'as':
        raise template.TemplateSyntaxError("third argument to '%s' tag must be 'as'" % bits[0])
    return GetUpcomingEventtimesNode(bits[1], bits[2], bits[4])



class GetFutureEventtimesNode(template.Node):
    def __init__(self, num, varname):
      self.num, self.varname = num, varname

    def render(self, context):
      now = datetime.datetime.now()
      context[self.varname] = EventTime.objects.filter(start_time__gte=now).order_by('start_time')[:self.num]
      return ''

@register.tag
def get_future_eventtimes(parser, token):
    """
    Retrieves a given number of upcoming EventTimes (events which start after the current date/time),
    sorted by start date.

    Syntax::

        {% get_future_eventtimes [num] as [varname] %}

    Example::

        {% get_future_eventtimes 5 as upcoming_eventtimes %}

    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'%s' tag takes three arguments" % bits[0])
    if bits[2] != 'as':
        raise template.TemplateSyntaxError("second argument to '%s' tag must be 'as'" % bits[0])
    return GetFutureEventtimesNode(bits[1], bits[3])
    
    
    
class GetPhotosForEventtimeNode(template.Node):
    def __init__(self, eventtime, varname, radius=None):
      self.eventtime, self.varname, self.radius = eventtime, varname, radius

    def render(self, context):
      from savoy.core.media.models import Photo
      from django.core.cache import cache
      
      self.eventtime = resolve_variable(self.eventtime, context)
      event_places = self.eventtime.event.places.all()
      
      if event_places:
        # First, check and see if we have this data in the cache. If so, return it.
        cache_key = "event-photos-" + str(self.radius) + "-" + self.eventtime.event.slug
      
        if type(cache.get(cache_key)) == type([]):
          context[self.varname] = cache.get(cache_key)
          return ''
      
        # If not, look it up.
        else:
          radius = float(self.radius)
          photo_content_type = ContentType.objects.get_for_model(Photo)
          photos_within_radius_ids = []
          for place in event_places:
            if place.location:
              photos_within_radius_geo_items = place.location().get_geolocated_items_within_radius(radius).filter(content_type=photo_content_type)
              for geo in photos_within_radius_geo_items:
                photos_within_radius_ids.append(geo.object_id)
          start_time = self.eventtime.start_time
          if self.eventtime.end_time:
            end_time = self.eventtime.end_time
          else:
            # If there is no end_time on the event, we assume the event went for 
            # the rest of the day, and into the morning (3am). This is not perfect at all,
            # but I don't know what else to do.
            end_date = self.eventtime.start_time + datetime.timedelta(days=1)
            end_time = datetime.datetime(year=self.eventtime.start_time.year, month=self.eventtime.start_time.month, day=end_date.day, hour=03, minute=00, second=00)
          photos_within_radius_and_date_range = Photo.objects.filter(id__in=photos_within_radius_ids).filter(date_created__range=(start_time, end_time))
          
          photo_list = []
        
        
          # This code ensures each photo's closet place is the place in question. In effect,
          # it ties every photo to exactly one place. After thinking about it, I decided I didn't want
          # this. But, I'm keeping it around, in in case I change my mind.
          
          # for photo in photos_within_radius_and_date_range:
          #   if photo.location is not None:
          #     for place in event_places:
          #       if photo.location.get_closest_place()['place'] == place:
          #           photo_list.append(photo)
        
          # This code, on the other hands, returns all photos in the radius, regardless of whether or
          # not this place is the closest one to the photo.
        
          for photo in photos_within_radius_and_date_range:
              photo_list.append(photo)
        
          # Save the data to the cache and then return it.
          cache.set(cache_key,photo_list,28800)
          context[self.varname] = photo_list
      
      return ''

@register.tag
def get_photos_for_eventtime(parser, token):
    """
    Retrieves photos likely taken at the event this eventtime refers to. Radius defaults to 25 miles if it is not given.

    Syntax::

        {% get_photos_for_eventtime [eventtime] as [varname] (with mile radius [miles]) %}

    Example::

        {% get_photos_for_eventtime eventtime as eventtime_photos with mile radius 1.5 %}

    """
    bits = token.contents.split()
    try:
      return GetPhotosForEventtimeNode(bits[1], bits[3], bits[7])
    except:
      return GetPhotosForEventtimeNode(bits[1], bits[3])
      
      
class GetStatusesForEventtimeNode(template.Node):
    def __init__(self, eventtime, varname):
      self.eventtime, self.varname = eventtime, varname

    def render(self, context):
      from savoy.contrib.statuses.models import Status
      self.eventtime = resolve_variable(self.eventtime, context)
      start_time = self.eventtime.start_time
      if self.eventtime.end_time:
        end_time = self.eventtime.end_time
      else:
        # If there is no end_time on the event, we assume the event went for 
        # the rest of the day, and into the morning (3am). This is not perfect at all,
        # but I don't know what else to do.
        end_date = self.eventtime.start_time + datetime.timedelta(days=1)
        end_time = datetime.datetime(year=self.eventtime.start_time.year, month=self.eventtime.start_time.month, day=end_date.day, hour=03, minute=00, second=00)
      statuses_within_date_range = Status.objects.filter(date_published__range=(start_time, end_time))
      context[self.varname] = statuses_within_date_range
      return ''

@register.tag
def get_statuses_for_eventtime(parser, token):
    """
    Retrieves statuses likely to have been posted at the event this eventtime refers to.

    Syntax::

        {% get_statuses_for_eventtime [eventtime] as [varname] %}

    Example::

        {% get_statuses_for_eventtime eventtime as eventtime_photos %}

    """
    bits = token.contents.split()
    return GetStatusesForEventtimeNode(bits[1], bits[3])