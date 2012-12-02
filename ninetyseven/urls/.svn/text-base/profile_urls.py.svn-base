from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from savoy.core.new.profiles.views import *
from ninetyseven.views import *
from ninetyseven.forms import *

urlpatterns = patterns('',
  url(
    regex   = r'^$',
    view    = people_index,
    name    = "people_index",
  ),
  url(
    regex   = r'^edit/$',
    view    = profile_edit,
    name    = 'profile_edit',
    kwargs  = {
      'profile_form_class': ProfileForm,
      'user_form_class': UserForm,
    }
  ),
  url(
    regex   = r'^(?P<username>[-\w]+)/beers/$',
    view    = user_beers_added,
    name    = "user_beers_added",
  ),
  url(
    regex   = r'^(?P<username>[-\w]+)/reviews/$',
    view    = user_reviews_added,
    name    = "user_reviews_added",
  ),
  url(
    regex   = r'^(?P<username>[-\w]+)/beers-recommended/$',
    view    = user_beers_recommended,
    name    = "user_beers_recommended",
  ),
  url(
    regex   = r'^top-contributors/$',
    view    = top_contributors,
    name    = "top_contributors",
  ),
  url(
    regex   = r'^new-users/$',
    view    = new_users,
    name    = "new_users",
  ),
  url(
    regex   = r'^(?P<username>[-\w]+)/$',
    view    = profile_detail,
    name    = 'profile_detail',
  ),
)