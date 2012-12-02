from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from savoy.core.pages.models import Page

# Create your views here.
def page_detail(request, template_dir="pages", extra_context={}):
    page = get_object_or_404(Page.live_pages, url=request.path)
    stripped_path = request.path.strip('/')
    context = {'page': page}
    if extra_context:
      for key, value in extra_context.items():
        if callable(value):
          context[key] = value()
        else:
          context[key] = value
    context = RequestContext(request, context)
    if page.template:
      return render_to_response((page.template.path, '%s/%s.html' % (template_dir, stripped_path), '%s/default.html' % template_dir), context)
    else:
      return render_to_response(('%s/%s.html' % (template_dir, stripped_path), '%s/default.html' % template_dir), context)
