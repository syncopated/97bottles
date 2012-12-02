from django.conf.urls.defaults import *
from ninetyseven.apps.relationships.views import *

urlpatterns = patterns('',
    url(
      regex = r'^follow_unfollow/(?P<to_user_id>\d+)/$',
      view  = follow_unfollow,
      name  = 'relationship_follow_unfollow',
    ),
)