from django.http import Http404, HttpResponseRedirect
from django.conf import settings

from savoy.core.pages.views import page_detail

class PageFallbackMiddleware(object):
  def process_response(self, request, response):
    if settings.APPEND_SLASH:
      if not request.path.endswith('/') and '.' not in request.path:
        redirect_path = '%s/' % request.path
        return HttpResponseRedirect(redirect_path)
      
    if response.status_code != 404:
      return response # No need to check for a flatpage for non-404 responses.
    try:
      return page_detail(request)
    # Return the original response if any errors happened. Because this
    # is a middleware, we can't assume the errors will be caught elsewhere.
    except Http404:
      return response
    except:
      if settings.DEBUG:
        raise
      return response
