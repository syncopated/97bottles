from django import template
from django.template import Library

from ninetyseven.apps.taglines.models import *

register = Library()

@register.simple_tag
def random_tagline():
  """
  Returns the text of a random tagline from the database.
  """
  try:
    tagline = Tagline.objects.all().order_by('?')[0].text
  except:
    tagline = None
  return tagline