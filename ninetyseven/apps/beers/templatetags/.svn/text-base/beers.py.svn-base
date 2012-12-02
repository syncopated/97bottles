import datetime

from django import template
from django.template import Library, Node
from django.contrib.contenttypes.models import ContentType
from django.template import resolve_variable
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache

register = Library()

Beer = models.get_model('beers', 'beer')
Brewery = models.get_model('beers', 'brewery')

class MostRecentBeersNode(template.Node):
  def __init__(self, num, variety, varname):
    self.num, self.category, self.varname = num, variety, varname

  def render(self, context):

    if self.category:
      category = resolve_variable(self.category, context)
      context[self.varname] = Beer.objects.for_variety(category).order_by('-date_created')[:self.num]
    else:
      context[self.varname] = Beer.objects.order_by('-date_created')[:self.num]

    return ''

@register.tag
def get_most_recent_beers(parser, token):
  """
  Returns the mostly recently added beers. If a variety is given,
  limits the results to only beers in that variety.

  Syntax::

      {% get_most_recent_beers [num] as [varname] %}
      {% get_most_recent_beers [num] from [variety] as [varname] %}

  Example::

      {% get_most_recent_beers 10 as most_recent_beers %}
      {% get_most_recent_beers 20 from variety as best_beers_in_variety %}

  """
  bits = token.contents.split()
  if len(bits) == 4:
    return MostRecentBeersNode(num=bits[1], varname=bits[3], variety=None)
  if len(bits) == 6:
    return MostRecentBeersNode(num=bits[1], variety=bits[3], varname=bits[5])


class HighestRatedBeersNode(template.Node):
  def __init__(self, num, variety, varname):
    self.num, self.category, self.varname = num, variety, varname

  def render(self, context):

    if self.category:
      category = resolve_variable(self.category, context)
      context[self.varname] = Beer.objects.for_variety(category).filter(rating__isnull=False).order_by('-rating')[:self.num]
    else:
      context[self.varname] = Beer.objects.filter(rating__isnull=False).order_by('-rating')[:self.num]

    return ''

@register.tag
def get_highest_rated_beers(parser, token):
  """
  Returns the highest rated beers. If a variety is given,
  limits the results to only beers in that variety.

  Syntax::

      {% get_highest_rated_beers [num] as [varname] %}
      {% get_highest_rated_beers [num] from [variety] as [varname] %}

  Example::

      {% get_highest_rated_beers 10 as top_rated_beers %}
      {% get_highest_rated_beers 20 from variety as best_beers_in_variety %}

  """
  bits = token.contents.split()
  if len(bits) == 4:
    return HighestRatedBeersNode(num=bits[1], varname=bits[3], variety=None)
  if len(bits) == 6:
    return HighestRatedBeersNode(num=bits[1], variety=bits[3], varname=bits[5])



class BeersForVarietyNode(template.Node):
  def __init__(self, category, varname):
    self.category, self.varname = category, varname

  def render(self, context):
    try:
      category = resolve_variable(self.category, context)
      context[self.varname] = Beer.objects.for_variety(category)
    except:
      pass
    return ''
  
@register.tag
def get_beers_for_variety(parser, token):
  """
  Returns beers for the given variety (a Category instance), 
  regardless of level of depth. That is to say, give "Ale", this
  will return all Ales, even those under "Ale: American Ale" 
  and "Ale: American Ale: American Amber / Red Ale".

  Syntax::

      {% get_beers_for_variety [category] as [varname] %}

  Example::

      {% get_beers_for_variety category as beer_list %}

  """
  bits = token.contents.split()
  if len(bits) != 4:
    raise template.TemplateSyntaxError("'%s' tag takes three arguments" % bits[0])
  if bits[2] != 'as':
    raise template.TemplateSyntaxError("fifth argument to '%s' tag must be 'as'" % bits[0])
  return BeersForVarietyNode(bits[1], bits[3])
  
  
  
class HighestRatedBreweriesNode(template.Node):
  def __init__(self, num, varname):
    self.num, self.varname = num, varname

  def render(self, context):
    context[self.varname] = Brewery.objects.filter(rating__isnull=False).order_by('-rating')[:self.num]
    return ''

@register.tag
def get_highest_rated_breweries(parser, token):
  """
  Returns the highest rated breweries.

  Syntax::

      {% get_highest_rated_breweries [num] as [varname] %}

  Example::

      {% get_highest_rated_breweries 10 as top_rated_breweries %}

  """
  bits = token.contents.split()
  if len(bits) == 4:
    return HighestRatedBreweriesNode(num=bits[1], varname=bits[3])
  else:
    raise template.TemplateSyntaxError("'%s' tag takes three arguments" % bits[0])
    
    
    
class TopContributorsNode(template.Node):
  def __init__(self, num, varname):
    self.num, self.varname = num, varname

  def render(self, context):
    context[self.varname] = User.objects.all().order_by('-info__contribution_score')[:self.num]
    return ''

@register.tag
def get_top_contributors(parser, token):
  """
  Returns the top contributors on the site.

  Syntax::

      {% get_top_contributors [num] as [varname] %}

  Example::

      {% get_top_contributors 10 as top_contributors %}

  """
  bits = token.contents.split()
  if len(bits) == 4:
    return TopContributorsNode(num=bits[1], varname=bits[3])
  else:
    raise template.TemplateSyntaxError("'%s' tag takes three arguments" % bits[0])
    
    

class MostInterestingBeersNode(template.Node):
  def __init__(self, num, varname):
    self.num, self.varname = num, varname

  def render(self, context):
    cache_key = 'most_interesting_beers_%s' % str(self.num)
    most_interesting_beers = cache.get(cache_key)
    if not most_interesting_beers:
      cache.add(cache_key, Beer.objects.all().order_by('-interestingness')[:self.num], 14400)
      most_interesting_beers = cache.get(cache_key)
    context[self.varname] = most_interesting_beers
    return ''

@register.tag
def get_most_interesting_beers(parser, token):
  """
  Returns the top contributors on the site.

  Syntax::

      {% get_most_interesting_beers [num] as [varname] %}

  Example::

      {% get_most_interesting_beers 10 as most_interesting_beers %}

  """
  bits = token.contents.split()
  if len(bits) == 4:
    return MostInterestingBeersNode(num=bits[1], varname=bits[3])
  else:
    raise template.TemplateSyntaxError("'%s' tag takes three arguments" % bits[0])

    
class RandomInterestingBeerNode(template.Node):
  def __init__(self, varname):
    self.varname = varname

  def render(self, context):
    try:
      import random
      interesting_beers = Beer.objects.all().order_by('-interestingness')[:20]
      index = random.randint(0, 19)
      context[self.varname] = interesting_beers[index]
    except:
      pass
    return ''

@register.tag
def get_random_interesting_beer(parser, token):
  """
  Returns one of the top 20 most interesting beers, randomly.

  Syntax::

      {% get_random_interesting_beer as [varname] %}

  Example::

      {% get_random_interesting_beer as interesting_beer %}

  """
  bits = token.contents.split()
  if len(bits) == 3:
    return RandomInterestingBeerNode(bits[2])
  else:
    raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    
    
    
class AllBeersNode(template.Node):
  def __init__(self, varname):
    self.varname = varname

  def render(self, context):
    try:
      context[self.varname] = Beer.objects.all().order_by('-rating')
    except:
      pass
    return ''

@register.tag
def get_all_beers(parser, token):
  """
  Returns all beers, ordered by rating (highest first).

  Syntax::

      {% get_all_beers as [varname] %}

  Example::

      {% get_all_beers as beer_list %}

  """
  bits = token.contents.split()
  if len(bits) == 3:
    return AllBeersNode(bits[2])
  else:
    raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    
    
    
    
class AllBreweriesNode(template.Node):
  def __init__(self, varname):
    self.varname = varname

  def render(self, context):
    try:
      context[self.varname] = Brewery.objects.all().order_by('-rating')
    except:
      pass
    return ''

@register.tag
def get_all_breweries(parser, token):
  """
  Returns all breweries, ordered by rating (highest first).

  Syntax::

      {% get_all_breweries as [varname] %}

  Example::

      {% get_all_breweries as brewery_list %}

  """
  bits = token.contents.split()
  if len(bits) == 3:
    return AllBreweriesNode(bits[2])
  else:
    raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])