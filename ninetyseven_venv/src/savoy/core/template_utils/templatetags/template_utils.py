from django import template
from django.template import Variable, Library, Node
from django.conf import settings
from django.utils.encoding import force_unicode

import datetime
import re


register = Library()

#
# Tags
#
###############################################################################

@register.simple_tag
def setting(name):
    return str(settings.__getattr__(name))

@register.simple_tag
def content_type_id(object):
    from django.contrib.contenttypes.models import ContentType
    content_type = ContentType.objects.get_for_model(object)
    return content_type.id



#
# Inclusion tags
#
###############################################################################

@register.inclusion_tag('includes/paginator.html', takes_context=True)
def paginator(context, adjacent_pages=2):
  """
  To be used in conjunction with the object_list generic view.

  Adds pagination context variables for use in displaying first, adjacent and
  last page links in addition to those created by the object_list generic
  view.
  
    {% paginator %}

  """
  page_numbers = [n for n in \
                  range(context['page'] - adjacent_pages, context['page'] + adjacent_pages + 1) \
                  if n > 0 and n <= context['pages']]
  return {
    'hits': context['hits'],
    'results_per_page': context['results_per_page'],
    'page': context['page'],
    'pages': context['pages'],
    'page_numbers': page_numbers,
    'next': context['next'],
    'previous': context['previous'],
    'has_next': context['has_next'],
    'has_previous': context['has_previous'],
    'show_first': 1 not in page_numbers,
    'show_last': context['pages'] not in page_numbers,
  }


#
# Filters
#
###############################################################################

@register.filter
def strip_newlines(value):
  value = value.replace('\n', ' ')
  value = value.replace('\r', ' ')
  return value


@register.filter
def word_count(value):
  """Returns the number of words in a string."""
  from django.utils.encoding import force_unicode
  value = force_unicode(value)
  words = value.split()
  return len(words)


@register.filter
def leading_zeros(value, desired_digits):
  """
  Given an integer, returns a string representation, padding with [desired_digits] zeros.
  """
  num_zeros = int(desired_digits) - len(str(value))
  padded_value = []
  while num_zeros >= 1:
    padded_value.append("0") 
    num_zeros = num_zeros - 1
  padded_value.append(str(value))
  return "".join(padded_value)
    


@register.filter
def days_since(value):
  """
  Returns number of days between today and value as a nicely formatted string.
    
    {% entry.pub_date|days_since %}
  
  """
  today = datetime.date.today()
  difference  = today - value
  if difference.days > 1:
    return '%s days ago' % difference.days
  elif difference.days == 1:
    return 'yesterday'
  elif difference.days == 0:
    return 'today'
  else:
    return value


@register.filter
def days_since_int(value):
  """
  Returns number of days between today and value as an integer.
    
    {% entry.pub_date|days_since_int %}
  
  """
  today = datetime.date.today()
  try:
    difference = today - value
  except:
    difference = today - value.date()
  return difference.days

@register.filter
def fuzzy_time(time):
  """
  Formats a time as fuzzy periods of the day.
  Accepts a datetime.time or datetime.datetime object.
  
    {% entry.pub_date|fuzzy_time %}
  
  """
  from bisect import bisect
  periods = ["Early-Morning", "Morning", "Mid-day", "Afternoon", "Evening", "Late-Night"]
  breakpoints = [4, 10, 13, 17, 21]
  try:
    return periods[bisect(breakpoints, time.hour)]
  except AttributeError: # Not a datetime object
    return '' #Fail silently
            


@register.filter
def get_links(value):
  """
  Returns links found in an (X)HTML string as Python objects for iteration in templates.

    <ul>
      {% for link in object.body|markdown|get_links %}
        <li><a href="{{ link.href }}">{{ link.title }}</a></li>
      {% endfor %}
    </ul>

  """
  
  try:
    from BeautifulSoup import BeautifulSoup
    import urllib2
  except ImportError:
    if settings.DEBUG:
      raise template.TemplateSyntaxError, "Error in {% get_links %} filter: The Python BeautifulSoup and/or urllib2 libraries aren't installed."
    return value
  soup = BeautifulSoup(value)
  return soup.findAll('a')

@register.filter
def is_vertical(url):
  """Given a URL to a photo, returns True is the photo is portrait in orientation."""
  if image_height(url) > image_width(url):
    return True
  else:
    return False



@register.filter
def is_horizontal(url):
  """Given a URL to a photo, returns True is the photo is landscape in orientation."""
  if image_width(url) > image_height(url):
    return True
  else:
    return False
        
        
@register.filter
def truncate_characters(s, num):
  "Truncates a string after a certain number of characters."
  s = force_unicode(s)
  length = int(num)
  if len(s) > length:
    string = s[:length]
    if not s[-1].endswith('...'):
      s = "%s%s" % (string, '...')
  return s


@register.filter
def unsmartypants(value):
  """
  Normalizes a string which has been processed by smartypants.py.
    
    {% entry.body|smartypants|unsmartypants %}
  
  """
  try:
    import smartypants
  except ImportError:
    if settings.DEBUG:
      raise template.TemplateSyntaxError, "Error in {% smartypants %} filter: The Python SmartyPants library isn't installed."
      return value
    else:
      return smartypants.smartyPants(value, '-1')



@register.filter
def widont(value):
  """
  Replaces the final space in a string with a non-breaking space to avoid
  typographic widows.
    
    {% entry.title|widont %}
  
  """
  return '&nbsp;'.join(value.rsplit(' ', 1))



@register.filter
def fractions(value):
  """
  Replaces ASCII fractions in a string with proper unicode versions.
    
    {% entry.body|fractions %}
  
  """
  FRACTION_MAPPING = {
     u'1/2' : u'\u00BD',
     u'1/4' : u'\u00BC',
     u'3/4' : u'\u00BE',
     u'1/3' : u'\u2153',
     u'2/3' : u'\u2154',
     u'1/5' : u'\u2155',
     u'2/5' : u'\u2156',
     u'3/5' : u'\u2157',
     u'4/5' : u'\u2158',
     u'1/6' : u'\u2159',
     u'5/6' : u'\u215A',
     u'1/8' : u'\u215B',
     u'3/8' : u'\u215C',
     u'5/8' : u'\u215D',
     u'7/8' : u'\u215E',
  }
  FRACTION_RE = re.compile(ur'(?:(?<=\d) +)?('+ '|'.join(FRACTION_MAPPING.keys())+ ur')\b')
  return FRACTION_RE.sub(lambda match: FRACTION_MAPPING[match.group(1)], value)



@register.filter
def replace (string, args): 
  """
  Basic search and replace. Returns string with replacements.
    
    {% entry.body|replace:"apple,orange" %}
  
  """
  search  = args.split(args[0])[1]
  replace = args.split(args[0])[2]
  return re.sub(search, replace, string)



@register.filter
def truncateletters(value, arg):
  """
  Truncates a string after a given number of characters..
    
    {% entry.body|truncateletters:"50" %}
  
  """
  try:
    length = int(arg)
  except ValueError: # invalid literal for int()
    return value # Fail silently
  if not isinstance(value, basestring):
    value = str(value)

  if len(value) > length:
    truncated = value[:length]
    if not truncated.endswith('...'):
      truncated += '...'
      return truncated
    return value

@register.filter
def extract_list(value, arg):
    """
    Takes a list of dicts, returns a list of values for a single key.
    """
    var_resolve = Variable(arg).resolve
    decorated = [var_resolve(item) for item in value]
    return decorated
        

@register.filter
def partition(thelist, n):
  """
  Break a list into ``n`` pieces. The last list may be larger than the rest if
  the list doesn't break cleanly. That is::

  >>> l = range(10)

  >>> partition(l, 2)
  [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]

  >>> partition(l, 3)
  [[0, 1, 2], [3, 4, 5], [6, 7, 8, 9]]

  >>> partition(l, 4)
  [[0, 1], [2, 3], [4, 5], [6, 7, 8, 9]]

  >>> partition(l, 5)
  [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]
  
    {% for sublist in mylist|parition:"3" %}
      {% for item in sublist %}
        do something with {{ item }}
      {% endfor %}
    {% endfor %}

  """
  try:
    n = int(n)
    thelist = list(thelist)
  except (ValueError, TypeError):
    return [thelist]
  p = len(thelist) / n
  return [thelist[p*i:p*(i+1)] for i in range(n - 1)] + [thelist[p*(i+1):]]



@register.filter
def partition_horizontal(thelist, n):
  """
  Break a list into ``n`` peices, but "horizontally." That is, 
  ``partition_horizontal(range(10), 3)`` gives::

    [[1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [10]]
  """
    
  try:
    n = int(n)
    thelist = list(thelist)
  except (ValueError, TypeError):
    return [thelist]
  newlists = [list() for i in range(n)]
  for i, val in enumerate(thelist):
    newlists[i%n].append(val)
  return newlists



@register.filter
def unescape(value):
  """
  Undoes basic HTML escaping, including ", <, >, and &.
    
    {% entry.body|unescape %}
  
  """
  value = value.replace('&quot;', '"')
  value = value.replace('&lt;', '<')
  value = value.replace('&gt;', '>')
  value = value.replace('&amp;', '&')
  return value



@register.filter
def in_list(value,arg):
  """
  Returns true if the specified item is in the specified list.  
    
    {% if item|in_list:list %} 
      in list 
    {% else %} 
      not in list
    {% endif %}
  
  """
  return value in arg


@register.filter
def stop_shouting(value):
  """
  Lowercases parts of a string with too many consecutive uppercase
  letters, as determined by the ``SHOUTING_LENGTH`` setting.

  Non-alphabetic characters are ignored when determining consecutive
  uppercase characters.

  ``SHOUTING_LENGTH`` defaults to 7.
  
    {% comment.body|stop_shouting:"8" %}
  
  """
  try:
      shouting_length = settings.SHOUTING_LENGTH
  except AttributeError:
      shouting_length = 7

  chunks = []
  upper_buffer = []
  upper_count = 0

  for char in value:
    if char.islower():
      if upper_buffer:
        chunk = ''.join(upper_buffer)
        if upper_count >= shouting_length:
          if len(chunk) > 2 and chunk[-1].isupper() and not chunk[-2].isalpha():
            chunk = chunk[:-1].lower() + chunk[-1]
          else:
            chunk = chunk.lower()
        chunks.append(chunk)
        upper_count = 0
        upper_buffer = []
      chunks.append(char)
    else:
      if char.isupper():
        upper_count += 1
      upper_buffer.append(char)

  # catch remainder
  chunk = ''.join(upper_buffer)
  if upper_count >= shouting_length:
    chunk = chunk.lower()
  chunks.append(chunk)

  return ''.join(chunks)