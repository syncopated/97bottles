from django.conf.urls.defaults import *
from django.views.generic.date_based import *
from django.views.generic.list_detail import object_list, object_detail
from django.contrib.syndication.views import feed

from savoy.contrib.portfolio.models import *

project_archive = {
  'queryset': Project.objects.all(),
  'date_field': 'date_published',
  'allow_empty': True,
  'template_object_name': 'project',
}

project_detail = {
  'queryset': Project.objects.all(),
  'template_object_name': 'project',
  'slug_field': 'slug',
}

testimonial_list = {
  'queryset': Testimonial.objects.all(),
  'allow_empty': True,
  'template_object_name': 'testimonial',
}

urlpatterns = patterns('',
    url(
      regex   = 'testimonials/$',
      view    = object_list,
      name    = 'testimonial_list',
      kwargs  = testimonial_list,
    ),
    url(
      regex   = '^$',
      view    = archive_index,
      name    = 'project_index',
      kwargs  = dict(project_archive,
                  num_latest = 30,
                  template_object_name = 'projects',
                )
    ),
    url(
      regex   = '^(?P<year>\d{4})/$',
      view    = archive_year,
      name    = 'project_archive_year',
      kwargs  = dict(project_archive, 
                  make_object_list = True,
                ),
    ),
    url(
      regex   = '^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
      view    = archive_month,
      name    = 'project_archive_month',
      kwargs  = project_archive,
    ),
    url(
      regex   = '^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/$',
      view    = archive_day,
      name    = 'project_archive_day',
      kwargs  = project_archive,
    ),
    url(
      regex   = '^(?P<slug>[-\w]+)/$',
      view    = object_detail,
      name    = 'project_detail',
      kwargs  = project_detail,
    ),
)