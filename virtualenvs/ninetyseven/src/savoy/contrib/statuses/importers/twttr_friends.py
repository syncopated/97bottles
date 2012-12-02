from savoy.utils.path import append_third_party_path
append_third_party_path()

import twitter

from django.conf import settings

from savoy.contrib.statuses.importers.twttr import process_statuses

def update():
  api = twitter.Api(username=settings.TWITTER_USERNAME, password=settings.TWITTER_PASSWORD)
  statuses = api.GetFriendsTimeline(settings.TWITTER_USERNAME)
  process_statuses(statuses)

if __name__ == '__main__':
    update()

