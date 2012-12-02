import string,re

from django.conf import settings
from django.contrib.auth.views import login
from django.http import HttpResponseRedirect

class LoginRequiredMiddleware(object):
  """ If this middleware is used, one must be logged in to view ANY page on the site. """
  def __init__(self):
    self.require_login_path = getattr(settings, 'REQUIRE_LOGIN_PATH', '/accounts/login/')
  
  def process_request(self, request):
    r = re.compile('('+string.join(settings.REQUIRE_LOGIN_ALLOWED_URL_PREFIXES,'|')+')')
    allowed_url = r.match(request.path)
    if request.path != self.require_login_path and not allowed_url and request.user.is_anonymous():
      if request.POST:
        return login(request)
      else:
        return HttpResponseRedirect('%s?next=%s' % (self.require_login_path, request.path))
          
class StaffLoginRequiredMiddleware(object):
  """ If this middleware is used, one must be logged in as staff to view ANY page on the site. """
  def __init__(self):
    self.require_login_path = getattr(settings, 'REQUIRE_LOGIN_PATH', '/accounts/login/')
    self.ALLOWED_PATHS = (
      self.require_login_path,
      '/admin/',
    )

  def process_request(self, request):
    r = re.compile('('+string.join(settings.REQUIRE_LOGIN_ALLOWED_URL_PREFIXES,'|')+')')
    allowed_url = r.match(request.path)
    if request.path not in self.ALLOWED_PATHS and not allowed_url and not request.user.is_staff:
      if request.POST:
        return login(request)
      else:
        return HttpResponseRedirect('%s?next=%s' % (self.require_login_path, request.path))
                
class OffHours:
  def process_view(self, request, view_func, view_args, view_kwargs):
    """
    If this middleware is used, the site will be 'offline' during the hours specified in these settings:
    
    OFFHOURS_BEGIN              = time(17)                      # Site closes at 5PM
    OFFHOURS_END                = time(6)                       # Site re-opens at 7AM
    OFFHOURS_WEEKENDS           = True                          # Site closed all weekend long.
    OFFHOURS_ALLOW_ANON_URLS    = True                          # Allow access to anonymous URLs
    OFFHOURS_ANON_ALLOWED_URLS  = ('/some/url/','/some/url',)   # List of anon-allowed urls.
    """
    anon_urls_allowed = getattr(settings,'OFFHOURS_ALLOW_ANON_URLS',True)
    anon_urls = getattr(settings,'OFFHOURS_ANON_ALLOWED_URLS',[])
    weekends_allowed = getattr(settings,'OFFHOURS_WEEKENDS',False)
    now = datetime.now()
    if request.user.is_authenticated() and not request.user.is_staff:
      if not anon_urls_allowed or (anon_urls_allowed and not any(i in request.path for i in anon_urls)):
        if (now.hour >= settings.OFFHOURS_BEGIN.hour or now.hour < settings.OFFHOURS_END.hour) or (not weekends_allowed and now.weekday() in [5,6]):
          request.user.message_set.create(message="You do not have permission to access this site during off-hours.")
          if anon_urls_allowed:
            return HttpResponseRedirect(settings.LOGIN_URL)
          raise Http404()