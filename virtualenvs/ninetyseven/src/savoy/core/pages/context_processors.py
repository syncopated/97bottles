from savoy.core.pages.models import Page

def add_page(request):
  try:
    if request.path.endswith('/'):
      path = request.path
    else:
      path = "%s/" % request.path
    p = Page.objects.get(url=path)
    return {'page': p }
  except Page.DoesNotExist:
    return {'page': '' }
