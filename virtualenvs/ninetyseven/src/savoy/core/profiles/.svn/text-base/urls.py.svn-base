from django.conf.urls.defaults import *
from django.contrib.auth.models import User

from savoy.core.profiles.models import Profile
from savoy.core.profiles.views import *

profiles = {
  'queryset': Profile.objects.all(),
  'template_object_name': 'profile',
}

urlpatterns = patterns('',
  url(
    regex   = '^(?P<username>[-\w]+)/$',
    view    = profile_detail,
    name    = 'profile_detail',
  ),
  url(
    regex   = '^(?P<username>[-\w]+)/edit/$',
    view    = edit_profile,
    name    = 'edit_profile',
  ),
  url (
    regex   = '^$',
    view    = 'django.views.generic.list_detail.object_list',
    kwargs  = profiles,
    name    = 'profile_list',
  ),
)