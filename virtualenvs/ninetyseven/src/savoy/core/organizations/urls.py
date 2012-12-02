from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail

from savoy.core.organizations.models import *

organizations = {
    'queryset': Organization.objects.all(),
    'template_object_name': 'organization',
}

urlpatterns = patterns('',
    url(
      regex   = '^$',
      view    = object_list,
      name    = 'organization_list',
      kwargs  = dict(organizations, template_name="organizations/organization_list.html", allow_empty=True)
    ),
    url(
      regex   = '^(?P<slug>[-\w]+)/$',
      view    = object_detail,
      name    = 'organization_detail',
      kwargs  = dict(organizations, slug_field="slug", template_name="organizations/organization_detail.html")
    ),
)