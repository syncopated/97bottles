from django import template
from django.template import Library

from savoy.contrib.portfolio.models import *

register = Library()

class FeaturedTestimonialsNode(template.Node):
    def __init__(self, varname):
      self.varname = varname

    def render(self, context):
      try:
        testimonials = Testimonial.objects.filter(featured=True)
        context[self.varname] = testimonials
      except:
        pass
      return ''

@register.tag
def get_featured_testimonials(parser, token):
    """
    Retrieves the Testimonials marked as "featured", and stores them in a context variable.

    Syntax::

        {% get_featured_testimonials as [varname] %}

    Example::

        {% get_featured_testimonials as featured_testimonials_list %}

    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    if bits [1] != 'as':
        raise template.TemplateSyntaxError("first argument to '%s' tag must be 'as'" % bits[0])
    return FeaturedTestimonialsNode(bits[2])
