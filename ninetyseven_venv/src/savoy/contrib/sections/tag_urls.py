from django.conf.urls.defaults import *
from django.contrib.auth.models import User

from savoy.core.tags.utils.tags import tag_detail, tag_list

urlpatterns = patterns('',
  url(
    regex   = '^$',
    view    = tag_list,
    name    = 'tag_list',
  ),
  url(
    regex   = '^(?P<tag>[-\S\s]+)/$',
    view    = tag_detail,
    name    = 'tag_detail',
  ),
)