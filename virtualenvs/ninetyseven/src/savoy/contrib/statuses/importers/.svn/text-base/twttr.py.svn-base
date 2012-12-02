from savoy.utils.path import append_third_party_path
append_third_party_path()

import twitter
import feedparser
import time
import datetime

from django.conf import settings

from savoy.contrib.statuses.models import *

def process_statuses(statuses):
  time_difference = datetime.timedelta(hours=settings.UTC_OFFSET)
  print "Processing statuses...\n"
  for status in statuses:
    print "Found status by " + status.user.name
    savoy_twitter_user, created_savoy_twitter_user = TwitterUser.objects.get_or_create(user_id = status.user.id)
    if not created_savoy_twitter_user:
      print "\tUser exists in Savoy database, skipping..."
    else:
      print "\tUser does not exist in Savoy database..."
    savoy_twitter_user.user_name          = status.user.name
    savoy_twitter_user.screen_name        = status.user.screen_name
    savoy_twitter_user.location           = status.user.location
    savoy_twitter_user.description        = status.user.description
    savoy_twitter_user.profile_image_url  = status.user.profile_image_url
    savoy_twitter_user.url                = status.user.url
    savoy_twitter_user.save()
    print "\t\tSaved user..."
    try:
      savoy_twitter_status                = TwitterStatus.objects.get(twitter_status_id = str(status.id))
      print "\tStatus exists in Savoy database, updating..."
      savoy_status                        = savoy_twitter_status.status
      savoy_status.body                   = status.text
      savoy_status.date_published         = datetime.datetime.fromtimestamp(time.mktime(feedparser._parse_date(status.created_at))) + time_difference
      savoy_status.save()
      print "\t\tUpdated status..."
    except TwitterStatus.DoesNotExist:
      print "\tStatus does not exist in Savoy database, saving..."
      savoy_status = Status(
        body                              = status.text,
        date_published                    = datetime.datetime.fromtimestamp(time.mktime(feedparser._parse_date(status.created_at))) + time_difference
      )
      savoy_status.save()
      savoy_twitter_status = TwitterStatus(
        status                            = savoy_status,
        twitter_status_id                 = status.id,
        twitter_user                      = savoy_twitter_user,
      )
      savoy_twitter_status.save()
      print "\t\tSaved savoy TwitterStatus object..."


def update():
  api = twitter.Api()
  statuses = api.GetUserTimeline(settings.TWITTER_USERNAME, count=200)
  process_statuses(statuses)

if __name__ == '__main__':
    update()