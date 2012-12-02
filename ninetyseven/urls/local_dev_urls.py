from django.conf.urls.defaults import *
from django.views.static import serve
from django.conf import settings

urlpatterns = patterns('',
  url(
    regex   = r'^(?P<path>.*)$',
    view    = serve, 
    name    = 'serve',
    kwargs  = { 'document_root': settings.MEDIA_ROOT, 'show_indexes': True, }
  ),
)