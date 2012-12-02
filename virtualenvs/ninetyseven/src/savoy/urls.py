##############################################################################
###                      EXAMPLE SAVOY URLCONF                             ###
##############################################################################

from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.static import serve
from django.views.generic.simple import direct_to_template

admin.autodiscover()

# URL for homepage. You will likely replace this with your own view.
urlpatterns = patterns('',
  (r'^$',                         direct_to_template, {'template': 'homepage.html'}),
)

# URLs for Savoy apps
urlpatterns += patterns('',
  (r'^aggregator/',               include('savoy.contrib.aggregator.urls')),
  (r'^aggregator/search/',        include('savoy.contrib.aggregator.search_urls')),
  (r'^blog/',                     include('savoy.contrib.blogs.urls')),
  (r'^bookmarks/',                include('savoy.contrib.bookmarks.urls')),
  (r'^comments/',                 include('savoy.contrib.comments.urls')),
  (r'^events/',                   include('savoy.contrib.events.urls')),
  (r'^media/galleries/',          include('savoy.contrib.galleries.urls')),
  (r'^podcasts/',                 include('savoy.contrib.podcasts.urls')),
  (r'^portfolio/',                include('savoy.contrib.portfolio.urls')),
  (r'^search/',                   include('savoy.contrib.aggregator.search_urls')),
  (r'^sections/',                 include('savoy.contrib.sections.urls')),
  (r'^statuses/',                 include('savoy.contrib.statuses.urls')),
  (r'^locations/',                include('savoy.core.geo.urls')),
  (r'^media/',                    include('savoy.core.media.urls')),
  (r'^organizations/',            include('savoy.core.organizations.urls')),
  (r'^people/',                   include('savoy.core.people.urls')),
  (r'^profiles/',                 include('savoy.core.profiles.urls')),
)

# URLs for third party apps distributed with Savoy.
urlpatterns += patterns('',
  (r'^contact/',                  include('contact_form.urls')),
)

# URLs for Django admin.
urlpatterns += patterns('',
  (r'^admin/doc/',                include('django.contrib.admindocs.urls')),
  (r'^admin/(.*)',                admin.site.root),
)
