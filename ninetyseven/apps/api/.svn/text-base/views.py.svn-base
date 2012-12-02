from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.utils import simplejson
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User

try:
  from hashlib import sha1
except:
  from sha import new as sha1

# Response mimetypes
API_MIMETYPES = {
  'json': 'text/javascript',
  # 'xml': 'application/xhtml+xml',
  # 'python': 'text/x-python',
  # 'csv': 'text/csv',
  # 'rdf': 'application/rdf+xml',
  # 'pickle': 'application/octet-stream',
  # 'yaml': 'text/x-yaml',
  # 'html': 'text/html',
}

if settings.DEBUG:
  # Set visually friendly content types when debugging
  API_MIMETYPES.update({
    'pickle': 'text/plain',
    'python': 'text/plain',
    'yaml': 'text/plain',
    'csv': 'text/plain',
  })

class Forbidden(HttpResponseForbidden):
  """403 Response Forbidden Error"""
  def __init__(self, request, msg):
    HttpResponseForbidden.__init__(self,'<h1>403 Forbidden</h1><p>%s</p>'%msg)

class BadRequest(HttpResponseBadRequest):
  """400 Bad Request Error"""
  def __init__(self, request, msg):
    HttpResponseBadRequest.__init__(self, '<h1>400 Bad Request</h1><p>%s</p>'%msg)

def get_auth_constraints(user):
  """
  Generates the API limits and API cache timeout for a given user class.
  Returns (result_limit, cache_timeout)
  """
  authchain = ('superuser','staff','authenticated','anonymous')
  for authbit in authchain:
    auth = getattr(user, 'is_%s' % authbit)
    if auth==1 or (callable(auth) and auth()==True):
      return (settings.API_LIMITS[authbit],settings.API_CACHE[authbit])
  return (None,None)

def format_qs(q):
    """
    Utility method that formats a query string into Django QuerySet selectors.
    """
    kw = {}
    for k,v in q.items():
      if k.endswith('__in') and isinstance(v, basestring):
        v = v.split(',')
      kw[str(k)] = v
    return kw


def serialize_object_list(object_list, indent, jsoncallback, format, len_limit, serialize_method):
  # Create a list of serialized objects.
  # This expects a _serialize() method on the models you wish to make available, or
  # a passed-in serialize_method argument.
  serialized_objects = []
  if serialize_method: default_serialize_method=False
  else: default_serialize_method=True
  for obj in object_list:
    if not default_serialize_method:
      serialized_obj = serialize_method(obj)
    else:
      serialize_method = getattr(obj, "_serialize", None)
      serialized_obj = serialize_method()
    serialized_objects.append(serialized_obj)
      
  # Create the seralized data.
  # Right now, we only support JSON. This may change in the future.
  if format=="json":
    content = simplejson.dumps(serialized_objects, indent=indent, cls=DjangoJSONEncoder, sort_keys=True)
  
  # Check to make sure the JSON doesn't exceed the content length limit.
  content_length = len(content)
  if not len_limit is None and content_length > len_limit:
    return BadRequest(request, "Content length exceeds limit")
  
  # If there's a json callback given, attach it to the content.
  if jsoncallback:
    content = '%s(%s)'%(jsoncallback,content)
    
  return content
  

def list(request, api_version, queryset, username=None, user_field="created_by", format=settings.API_DEFAULT_FORMAT, paginate_by=50, serialize_method=None):
  """
  Serializes Django model instances based on the results of a method, which defaults to
  _serialize() on the model itself. You can pass in your own method, if you prefer (or,
  if you don't have access to the model). The serialize method should take the object, 
  and return the object as a Python dictionary. The format and presentation 
  of this dictionary is up to you. This view will then serialized based on the format
  of that dictionary.
  
  The view takes several possible query parameters, including offset, limit, indent level
  (json only), order_by, page, and jsoncallback. Any other params passed will be treated as
  QuerySet filters, and should be provided in Django QuerySet syntax 
  (i.e. name__icontains=whatever).
  """
  # Parse the query string for supported options.
  query         = dict(request.REQUEST.items())
  hash          = sha1(request.path+str(sorted(query))).hexdigest()
  offset        = int(query.pop('offset', 0))
  limit         = int(query.pop('limit', 1000000000000))
  indent        = int(query.pop('indent', 4))
  order_by      = query.pop('order_by', None)
  page          = query.pop('page', 1)
  jsoncallback  = str(query.pop('jsoncallback',''))
  
  # Check to make sure the requsted format is one of our options.
  try:
    response = HttpResponse(mimetype=API_MIMETYPES[format])
  except KeyError:
    return BadRequest(request, "No format found matching %s" % format)
    
  # Check the auth constraints for this user and make sure they're
  # not exceeding they're QuerySet limit.
  user = request.user
  (qs_limit,len_limit),timeout = get_auth_constraints(user)
  if not qs_limit is None and limit - offset > qs_limit:
    return BadRequest(request, 'Record limit exceded (%s)' % qs_limit)
  
  # Filter and order the Queryset.
  if len(query):
    queryset = queryset.filter(**format_qs(query))
  if order_by:
    queryset = queryset.order_by(*order_by.split(','))
  
  # If a username was provided, filter the QuerySet by that user.
  # This uses the user_field argument, as well. It defaults to
  # "created_by".
  if username:
    filter_user = get_object_or_404(User, username=username)
    if hasattr(queryset.model, user_field):
      kwargs = { "%s" % user_field: filter_user }
      queryset = queryset.filter(**kwargs)
  
  # Limit, and offset the QuerySet, creating the object_list.
  object_list = queryset.all()[offset:limit]
  
  # Paginate the object_list.
  paginator = Paginator(object_list, paginate_by)
  page_num = int(page)
  this_page = paginator.page(page_num)
  object_list = this_page.object_list
  
  # Serialize the object_list.
  content = serialize_object_list(object_list, indent, jsoncallback, format, len_limit, serialize_method)
  
  # Return the response.
  return HttpResponse(content, mimetype=API_MIMETYPES[format])
  
  
def detail(request, api_version, format, object_id, queryset, serialize_method=None):
  """
  Serialized a single object and returns it. Only takes one query parameter, indent, 
  which only works for json.
  """
  # Parse the query string for supported options.
  query = dict(request.REQUEST.items())
  indent = int(query.pop('indent', 4))
  jsoncallback  = str(query.pop('jsoncallback',''))
  
  # Check the auth constraints for this user.
  user = request.user
  (qs_limit,len_limit),timeout = get_auth_constraints(user)
  
  # Find the requested object.
  obj = get_object_or_404(queryset.model, pk=int(object_id))
  object_list = [obj]
  
  # Serialize the object_list.
  content = serialize_object_list(object_list, indent, jsoncallback, format, len_limit, serialize_method)
  
  return HttpResponse(content, mimetype=API_MIMETYPES[format])