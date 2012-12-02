from django.conf.urls.defaults import *
 
from ninetyseven.apps.reviews.views import *
 
urlpatterns = patterns('', 
  url(
      regex = r'^_edit/(?P<review_id>\d+)/$',
      view = edit_review,
      name = 'edit_review',
  ),
  url (
      regex = r'^post/$',
      view = post_review,
      name = 'post_review',
      ),
  url (
      regex = r'^recently_added/$',
      view = recently_added_reviews,
      name = 'recently_added_reviews',
      ),
  url (
      regex = r'^get_more_reviews/$',
      view  = get_more_reviews,
      name = 'get_more_reviews',
      ),
)