from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail

from savoy.core.people.models import *

people = {
    'queryset': Person.objects.all(),
    'template_object_name': 'person',
}

urlpatterns = patterns('',
  url(
    regex   = '^$',
    view    = object_list,
    name    = 'person_list',
    kwargs  = dict(people, template_name="people/person_list.html", allow_empty=True)
  ),
  url(
    regex   = '^(?P<slug>[-\w]+)/$',
    view    = object_detail,
    name    = 'person_detail',
    kwargs  = dict(people, template_name="people/person_detail.html", slug_field="slug")
  ),

)