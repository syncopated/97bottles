from django.conf.urls.defaults import *

from savoy.contrib.search.views import *

urlpatterns = patterns('',
  url(
    regex   = '^$',
    view    = perform_search,
    name    = 'perform_search',
  ),
)