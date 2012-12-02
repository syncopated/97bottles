from django.conf.urls.defaults import *
from django.db import models

from ninetyseven.apps.tell_a_friend.views import *

urlpatterns = patterns('',
  url(
    regex = r'^$',
    view = tell_a_friend,
    name = 'tell_a_friend',
  ),
)