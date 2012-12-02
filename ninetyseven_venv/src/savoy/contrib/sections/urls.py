from django.conf.urls.defaults import *
from django.contrib.auth.models import User

from savoy.contrib.sections.models import Section

sections = Section.objects.all()

urlpatterns = patterns('',
  url(
    regex   = '^(?P<slug>[-\w]+)/$',
    view    = 'django.views.generic.list_detail.object_detail',
    kwargs  = { 'queryset': sections, 'template_object_name': 'section' },
    name    = 'section_detail',
  ),
  url(
    regex   = '^$',
    view    = 'django.views.generic.list_detail.object_list',
    kwargs  = { 'queryset': sections, 'template_object_name': 'section' },
    name    = 'section_list',
  ),
)