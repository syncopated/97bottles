from django import template
from django.template import resolve_variable

from savoy.core.pages.models import Page

register = template.Library()

class GetPageByURLNode(template.Node):
    def __init__(self, url, varname):
      self.url, self.varname = url, varname

    def render(self, context):
      try:
        url = resolve_variable(self.url, context)
      except:
        url = self.url
      
      try:
        context[self.varname] = Page.objects.get(url=url)
      except:
        pass
      return ''

@register.tag
def get_page_by_url(parser, token):
    """
    Retrieves a specific page object by URL and assigns it to a context variable.

    Syntax::

        {% get_page_by_url [url] as [varname] %}

    Example::

        {% get_page_by_url /about/ as about_page %}

    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'%s' tag takes three arguments" % bits[0])
    if bits[2] != 'as':
        raise template.TemplateSyntaxError("second argument to '%s' tag must be 'as'" % bits[0])
    return GetPageByURLNode(bits[1], bits[3])