from django.conf.urls.defaults import *
from django.db import models
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from ninetyseven.apps.api.views import *
from ninetyseven.apps.beers.models import *

from faves.models import *

def fave_list(request, api_version, queryset, fave_type_slug, username=None, user_field="created_by", format=settings.API_DEFAULT_FORMAT, paginate_by=50, serialize_method=None):
  """
  Creates the unique QuerySet for a fave list and then passes it on to the
  standard api list view.
  """
  fave_type = get_object_or_404(FaveType, slug=fave_type_slug)
  user = get_object_or_404(User, username=username)
  faves = Fave.objects.get_for_user(user, fave_type=fave_type)
  content_type = ContentType.objects.get_for_model(queryset.model)
  object_id_list = [ fave.content_object.pk for fave in faves if fave.content_type==content_type ]
  queryset = queryset.filter(pk__in=object_id_list)
  username = None
  return list(request, api_version, queryset, username, user_field, format, paginate_by, serialize_method)

def recommendation_list(request, api_version, queryset, username=None, user_field="created_by", format=settings.API_DEFAULT_FORMAT, paginate_by=50, serialize_method=None):
  """
  API view for recommended beers. Since this is not a QuerySet and has a
  specific order, this has to be done a little differently, and can't use 
  the main generic view for API lists. 
  """
  user = get_object_or_404(User, username=username)
  recommendations = user.info.recommended_beers()
  
  # Parse the query string for supported options.
  query         = dict(request.REQUEST.items())
  hash          = sha1(request.path+str(sorted(query))).hexdigest()
  offset        = int(query.pop('offset', 0))
  limit         = int(query.pop('limit', 50))
  indent        = int(query.pop('indent', 4))
  jsoncallback  = str(query.pop('jsoncallback',''))
  
  # Check to make sure the requsted format is one of our options.
  try:
    response = HttpResponse(mimetype=API_MIMETYPES[format])
  except KeyError:
    return BadRequest(request, "No format found matching %s" % format)
    
  # Check the auth constraints for this user and make sure they're
  # not exceeding they're QuerySet limit. The view has a max QuerySet
  # limit of 50 (thus, it's never paginated).
  user = request.user
  (qs_limit,len_limit),timeout = get_auth_constraints(user)
  if qs_limit > 50:
    qs_limit=50
  if not qs_limit is None and limit - offset > qs_limit:
    return BadRequest(request, 'Record limit exceded (%s)' % qs_limit)

  object_list = recommendations[offset:limit]
  content = serialize_object_list(object_list, indent, jsoncallback, format, len_limit, serialize_method)

  # Return the response.
  return HttpResponse(content, mimetype=API_MIMETYPES[format])


urlpatterns = patterns('',
  # Beers
  url(
    regex = r'^v(?P<api_version>\d+)/(?P<format>[-\w]+)/beers/$',
    view = list,
    name = 'api_beer_list',
    kwargs = {
      'queryset': Beer.objects.all(),
    },
  ),
  url(
    regex = r'^v(?P<api_version>\d+)/(?P<format>[-\w]+)/beers/(?P<object_id>\d+)/$',
    view = detail,
    name = 'api_beer_detail',
    kwargs = {
      'queryset': Beer.objects.all(),
    },
  ),
  url(
    regex = r'^v(?P<api_version>\d+)/(?P<format>[-\w]+)/beers/(?P<username>[-\w]+)/$',
    view = list,
    name = 'api_beer_list_for_user',
    kwargs = {
      'queryset': Beer.objects.all(),
    },
  ),
  url(
    regex = r'^v(?P<api_version>\d+)/(?P<format>[-\w]+)/beers/(?P<username>[-\w]+)/beers-recommended/$',
    view = recommendation_list,
    name = 'api_beer_recommendation_list_for_user',
    kwargs = {
      'queryset': Beer.objects.all(),
    },
  ),
  url(
    regex = r'^v(?P<api_version>\d+)/(?P<format>[-\w]+)/beers/(?P<username>[-\w]+)/(?P<fave_type_slug>[-\w]+)/$',
    view = fave_list,
    name = 'api_beer_fave_list_for_user',
    kwargs = {
      'queryset': Beer.objects.all(),
    },
  ),
  
  # Breweries
  url(
    regex = r'^v(?P<api_version>\d+)/(?P<format>[-\w]+)/breweries/$',
    view = list,
    name = 'api_brewery_list',
    kwargs = {
      'queryset': Brewery.objects.all(),
    },
  ),
  url(
    regex = r'^v(?P<api_version>\d+)/(?P<format>[-\w]+)/breweries/(?P<object_id>\d+)/$',
    view = detail,
    name = 'api_brewery_detail',
    kwargs = {
      'queryset': Brewery.objects.all(),
    },
  ),
  url(
    regex = r'^v(?P<api_version>\d+)/(?P<format>[-\w]+)/breweries/(?P<username>[-\w]+)/$',
    view = list,
    name = 'api_brewery_list_for_user',
    kwargs = {
      'queryset': Brewery.objects.all(),
    },
  ),
  
  # Reviews
  url(
    regex = r'^v(?P<api_version>\d+)/(?P<format>[-\w]+)/reviews/$',
    view = list,
    name = 'api_review_list',
    kwargs = {
      'queryset': Review.objects.all(),
    },
  ),
  url(
    regex = r'^v(?P<api_version>\d+)/(?P<format>[-\w]+)/reviews/(?P<object_id>\d+)/$',
    view = detail,
    name = 'api_review_detail',
    kwargs = {
      'queryset': Review.objects.all(),
    },
  ),
  url(
    regex = r'^v(?P<api_version>\d+)/(?P<format>[-\w]+)/reviews/(?P<username>[-\w]+)/$',
    view = list,
    name = 'api_review_list_for_user',
    kwargs = {
      'queryset': Review.objects.all(),
    },
  ),
)