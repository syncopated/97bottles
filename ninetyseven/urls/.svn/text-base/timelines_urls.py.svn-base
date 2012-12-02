from django.conf.urls.defaults import *
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db import models

Relationship = models.get_model('relationships','relationship')
UserTimelineItem = models.get_model('timelines','usertimelineitem')
import timelines.views

def timelines_following_archive(request, username):
  user = get_object_or_404(User, username=username)
  following = [ relationship.to_user for relationship in Relationship.objects.relationships_for_user(user)['friends']]
  following_timeline_items = UserTimelineItem.objects.filter(user__in=following)
  return timelines.views.archive(request, following_timeline_items, extra_context={ 'following_timeline': user })

def timelines_following_year(request, username, year):
  user = get_object_or_404(User, username=username)
  following = [ relationship.to_user for relationship in Relationship.objects.relationships_for_user(user)['friends']]
  following_timeline_items = UserTimelineItem.objects.filter(user__in=following)
  return timelines.views.year(request, year, following_timeline_items, extra_context={ 'following_timeline': user })

def timelines_following_month(request, username, year, month):
  user = get_object_or_404(User, username=username)
  following = [ relationship.to_user for relationship in Relationship.objects.relationships_for_user(user)['friends']]
  following_timeline_items = UserTimelineItem.objects.filter(user__in=following)
  return timelines.views.month(request, year, month, following_timeline_items, extra_context={ 'following_timeline': user })

def timelines_following_day(request, username, year, month, day):
  user = get_object_or_404(User, username=username)
  following = [ relationship.to_user for relationship in Relationship.objects.relationships_for_user(user)['friends']]
  following_timeline_items = UserTimelineItem.objects.filter(user__in=following)
  return timelines.views.day(request, year, month, day, following_timeline_items, extra_context={ 'following_timeline': user })

def timelines_following_today(request, username):
  user = get_object_or_404(User, username=username)
  following = [ relationship.to_user for relationship in Relationship.objects.relationships_for_user(user)['friends']]
  following_timeline_items = UserTimelineItem.objects.filter(user__in=following)
  return timelines.views.today(request, following_timeline_items, extra_context={ 'following_timeline': user })

# URLs for third party apps.
urlpatterns = patterns('',
  url(
      regex = r"^people/(?P<username>[-\w]+)/beer-log/following/$",
      view  = timelines_following_archive,
      name  = "timelines_following_archive",
  ),
  url(
      regex = r"^people/(?P<username>[-\w]+)/beer-log/following/today/$",
      view  = timelines_following_today,
      name  = "timelines_following_today",
  ),
  url(
      regex = r"^people/(?P<username>[-\w]+)/beer-log/following/(?P<year>\d{4})/$",
      view  = timelines_following_year,
      name  = "timelines_following_year",
  ),
  url(
      regex = r"^people/(?P<username>[-\w]+)/beer-log/following/(?P<year>\d{4})/(?P<month>\w{3})/$",
      view  = timelines_following_month,
      name  = "timelines_following_month",
  ),
  url(
      regex = r"^people/(?P<username>[-\w]+)/beer-log/following/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$",
      view  = timelines_following_day,
      name  = "timelines_following_day",
  ),
  (r'^people/(?P<username>[-\w]+)/beer-log/',   include('timelines.urls.user')),
  (r'^beer-log/',                               include('timelines.urls.site')),
)