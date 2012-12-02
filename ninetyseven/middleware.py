from django.conf import settings

class MobileMiddleware(object):
  def process_request(self, request):
    domain = request.META.get('HTTP_HOST', '').split('.')
    if 'm' in domain or 'mobile' in domain or 'devmobile' in domain:
      settings.TEMPLATE_DIRS = settings.MOBILE_TEMPLATE_DIRS
      settings.CACHE_MIDDLEWARE_KEY_PREFIX = settings.MOBILE_CACHE_KEY_PREFIX
    else:
      settings.TEMPLATE_DIRS = settings.DESKTOP_TEMPLATE_DIRS
      settings.CACHE_MIDDLEWARE_KEY_PREFIX = settings.DESKTOP_CACHE_KEY_PREFIX