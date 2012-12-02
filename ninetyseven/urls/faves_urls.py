from django.conf.urls.defaults import *

from faves.views import *

urlpatterns = patterns('',
  url(
    regex   = '^users/(?P<username>[-\w]+)/(?P<fave_type_slug>[-\w]+)/$',
    view    = user_faves,
    name    = 'user_faves',
  ),
)