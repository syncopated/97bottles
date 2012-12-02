from django.conf.urls.defaults import *
from django.contrib.syndication.views import feed

from ninetyseven.apps.beers.feeds import *
from ninetyseven.apps.reviews.feeds import *

from timelines.feeds import *
from ninetyseven.feeds import *

feeds = {
  'latest-beers':             LatestBeers,
  'latest-beers-for-brewery': LatestBeersPerBrewery,
  'latest-breweries':         LatestBreweries,
  'latest-reviews':           LatestReviews,
  'latest-reviews-for-beer':  LatestReviewsPerBeer,
  'beer-log':                 LatestUserTimelineItems,
  'beer-log-for-person':      LatestUserTimelineItemsPerUser,
  'beer-log-for-following':   LatestUserTimelineItemsForFollowing,
}

urlpatterns = patterns('',
  url(
    regex   = '^(?P<url>.*)/$',
    view    = feed,
    kwargs  = { 'feed_dict': feeds },
    name    = 'feeds',
  )
)