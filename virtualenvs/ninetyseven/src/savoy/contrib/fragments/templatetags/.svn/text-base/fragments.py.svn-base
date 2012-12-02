from django import template
from django.db import models
from django.core.cache import cache
from savoy.contrib.fragments.models import Fragment

register = template.Library()

CACHE_PREFIX = "fragment_"

def get_fragment(parser, token):
  """
  Pulls the specified fragment from either the cache or the database, passes
  it through the appropriate markup filter, and then outputs the content into
  the template. Requires fragment key argument and optionally takes a number
  of seconds to cache the fragment for.
  
  Usage:
  {% fragment "fragment-key" [seconds] %}
  
  Example:
  {% fragment "my-fragment" 300 %}
  """
  # split_contents() knows not to split quoted strings.
  tokens = token.split_contents()
  if len(tokens) < 2 or len(tokens) > 3:
    raise template.TemplateSyntaxError, "%r tag should have either 2 or 3 arguments" % (tokens[0],)
  if len(tokens) == 2:
    tag_name, key = tokens
    cache_time = 0
  if len(tokens) == 3:
    tag_name, key, cache_time = tokens
  # Check to see if the key is properly double/single quoted
  if not (key[0] == key[-1] and key[0] in ('"', "'")):
    raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
  # Send key without quotes and caching time
  return FragmentNode(key[1:-1], cache_time)
    
class FragmentNode(template.Node):
  def __init__(self, key, cache_time=0):
    self.key = key
    self.cache_time = cache_time
  
  def render(self, context):
    from django.contrib.markup.templatetags.markup import markdown, textile, restructuredtext
    try:
      cache_key = CACHE_PREFIX + self.key
      fragment = cache.get(cache_key)
      
      if fragment is None:
        fragment = Fragment.objects.get(key=self.key)
        cache.set(cache_key, fragment, int(self.cache_time))

      if fragment.markup_language == 'markdown':
        content = markdown(fragment.content)
      elif fragment.markup_language == 'textile':
        content = textile(fragment.content)
      elif fragment.markup_language == 'restructured_text':
        content = restructured_text(fragment.content)
      else:
        content = fragment.content
      
      return content
    except Fragment.DoesNotExist:
      return ''
        
register.tag('fragment', get_fragment)