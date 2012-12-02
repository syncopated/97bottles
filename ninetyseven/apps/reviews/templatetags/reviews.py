from django import template
from django.db import models
from django.template import resolve_variable

from ninetyseven.apps.reviews.forms import *
from ninetyseven.apps.beers.forms import *

register = template.Library()

Review = models.get_model("reviews","review")

@register.inclusion_tag('reviews/review_list.html', takes_context=True)
def render_review_list(context, beer):
  """
  Renders the list of reviews for a given beer.

  {% render_review_list beer %}
  """
  reviews = Review.objects.filter(beer=beer).order_by('date_submitted')
  return {
    'user': context['request'].user,
    'review_list': reviews,
  }

@register.inclusion_tag('reviews/review_form.html', takes_context=True)
def render_review_form(context, beer):
  """
  Renders the review form for a given beer.
  
  {% render_review_form beer %}
  """
  if context.has_key('preview'):
    preview = True
  else:
    preview = False
    
  return {
    'user': context['request'].user,
    'beer': beer,
    'preview': preview,
    'review_form': ReviewForm(initial={'beer': beer.id }, instance=Review(), prefix="review"),
    'city_form': CityForm(instance=City(), prefix="city"),
  }

@register.inclusion_tag('reviews/review_form_mobile.html', takes_context=True)
def render_review_form_mobile(context, beer):
    """
    Renders the review form for a given beer for mobile (Omits City)

    {% render_review_form_mobile beer %}
    """
    if context.has_key('preview'):
      preview = True
    else:
      preview = False

    return {
      'user': context['request'].user,
      'beer': beer,
      'preview': preview,
      'review_form': ReviewForm(initial={'beer': beer.id }, instance=Review(), prefix="review"),
      'city_form': CityForm(instance=City(), prefix="city"),
    }
  
class RecentReviewsNode(template.Node):
  def __init__(self, num, variety, varname):
    self.num, self.category, self.varname = num, variety, varname

  def render(self, context):
    from ninetyseven.apps.reviews.models import Review
    if self.category:
      category = resolve_variable(self.category, context)
      context[self.varname] = Review.objects.filter(beer__variety=category).order_by('-date_created')[:self.num]
    else:
      context[self.varname] = Review.objects.order_by('-date_created')[:self.num]

    return ''

@register.tag
def get_most_recent_reviews(parser, token):
  """
  Returns the most recent reviews. If a variety is given,
  limits the results to only reviews of beers in that variety.

  Syntax::

      {% get_most_recent_reviews [num] as [varname] %}
      {% get_most_recent_reviews [num] from [variety] as [varname] %}

  Example::

      {% get_most_recent_reviews 10 as recent_reviews %}
      {% get_most_recent_reviews 20 from variety as recent_reviews_in_variety %}

  """
  bits = token.contents.split()
  if len(bits) == 4:
    return RecentReviewsNode(num=bits[1], varname=bits[3], variety=None)
  if len(bits) == 6:
    return RecentReviewsNode(num=bits[1], variety=bits[3], varname=bits[5])
    
    
    
class GetBeerReviewForUserNode(template.Node):
  def __init__(self, beer, user, varname):
    self.beer, self.user, self.varname = beer, user, varname

  def render(self, context):
    from ninetyseven.apps.reviews.models import Review
    beer = resolve_variable(self.beer, context)
    user = resolve_variable(self.user, context)
    try:
      context[self.varname] = Review.objects.get(created_by=user, beer=beer)
    except:
      context[self.varname] = None
    return ''

@register.tag
def get_beer_review_for_user(parser, token):
  """
  Returns the give user's review for the given beer. If the review doesn't exist, returns none.

  Syntax::

      {% get_beer_review_for_user [beer] [user] as [varname] %}

  Example::

      {% get_beer_review_for_user beer user as review %}

  """
  bits = token.contents.split()
  if len(bits) == 5:
    return GetBeerReviewForUserNode(beer=bits[1], user=bits[2], varname=bits[4])
    
@register.filter
def a_or_an_for_int(value):
  an_ints = (8,11,18,80,81,82,83,84,85,86,87,88,89)
  if value in an_ints:
    return "an"
  else:
    return "a"