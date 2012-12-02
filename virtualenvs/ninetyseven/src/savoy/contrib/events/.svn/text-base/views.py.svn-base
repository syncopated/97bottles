import datetime
import time

from django.http import Http404
from django.template.loader import get_template
from django.shortcuts import render_to_response

from savoy.contrib.events.models import *
from savoy.core.people.models import *


def eventtime_detail(request, year, month, day, slug, eventtime_id):
  from django.views.generic.list_detail import object_detail
  
  try:
    event       = Event.objects.get(slug=slug)
    eventtimes  = EventTime.objects.all()
    eventtime   = EventTime.objects.get(id=eventtime_id)
  except (Event.DoesNotExist, EventTime.DoesNotExist,):
    raise Http404
  
  return object_detail(
    request, 
    queryset=eventtimes,
    object_id=eventtime_id,
    template_object_name='eventtime',
  )