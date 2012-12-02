from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail

from savoy.contrib.galleries.models import *
from savoy.contrib.galleries.views import *

gallery_list = {
    'queryset': Gallery.objects.all(),
    'template_object_name': 'gallery',
    'template_name': 'galleries/gallery_list.html',
    'allow_empty': True,
}

urlpatterns = patterns('',    
    url(
      regex   = '^$',
      view    = object_list,
      name    = 'gallery_list',
      kwargs  = gallery_list,
    ),
    url(
      regex   = '(?P<slug>[-\w]+)/$',
      view    = gallery_detail,
      name    = 'gallery_detail',
    ),
)
