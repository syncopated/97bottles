from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.static import serve
from django.views.generic.simple import direct_to_template
from django.conf import settings

import haystack

admin.autodiscover()
haystack.autodiscover()

urlpatterns = patterns('',
  (r'^sections/',                                 include('savoy.contrib.sections.urls')),
  (r'^comments/',                                 include('django.contrib.comments.urls')),
  (r'^tell-a-friend/',                            include('ninetyseven.apps.tell_a_friend.urls')),
  (r'^invites/',                                  include('ninetyseven.apps.invites.urls')),
  (r'^people/',                                   include('ninetyseven.urls.profile_urls')),
  (r'^preferences/',                              include('ninetyseven.apps.preferences.urls')),
  (r'^blog/',                                     include('savoy.contrib.blogs.urls')),
  (r'^search/',                                   include('ninetyseven.apps.search.urls')),
  (r'^admin/doc/',                                include('django.contrib.admindocs.urls')),
  (r'^admin/(.*)',                                admin.site.root),
  (r'^contact/',                                  include('contact_form.urls')),
  (r'^favorites/',                                include('faves.urls')),
  (r'^account/',                                  include('django_authopenid.urls')),
  (r'^people/(?P<username>[-\w]+)/relationships/',include('ninetyseven.apps.relationships.urls.user_relationships')),
  (r'^relationships/',                            include('ninetyseven.apps.relationships.urls.follow_unfollow')),
  (r'^breweries/',                                include('ninetyseven.apps.beers.urls.breweries')),
  (r'^reviews/',                                  include('ninetyseven.apps.reviews.urls')),
  (r'^tags/',                                     include('ninetyseven.apps.tags.urls')),
  (r'^pages/',                                    include('savoy.core.pages.urls')),
  (r'^feeds/',                                    include('ninetyseven.urls.feeds_urls')),
  (r'^api/',                                      include('ninetyseven.apps.api.urls')),
)

if settings.LOCAL_DEV:
  # URLs for serving static files with Django. This should only be used for development.
  urlpatterns += patterns('',
    (r'^static/',                                  include('ninetyseven.urls.local_dev_urls')),
  )

urlpatterns += patterns('',
  (r'^',                                          include('ninetyseven.urls.timelines_urls')),
  (r'^',                                          include('ninetyseven.urls.faves_urls')),
  (r'^',                                          include('ninetyseven.urls.misc_urls')),
  (r'^',                                          include('ninetyseven.apps.beers.urls.beers')),
)
