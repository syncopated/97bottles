from django.conf.urls.defaults import *

from ninetyseven.apps.relationships.views import *

urlpatterns = patterns('',
  url(
    regex   = '^$',
    view    = user_relationships,
    name    = 'user_relationships',
  ),
)