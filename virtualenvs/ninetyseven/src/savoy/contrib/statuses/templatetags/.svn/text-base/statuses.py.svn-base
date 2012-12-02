import datetime
import re

from django import template
from django.template import Library
from django.template import resolve_variable
from django.utils.safestring import mark_safe

from savoy.contrib.statuses.models import *

register = Library()

@register.filter
def link_mentions(value):
  """
  Finds all @ references and links them to their respective Twitter profile pages.
  
  Example::
    
    {{ object.quote|link_mentions }}
    
  """
  try:
    new_value = re.sub(r'(@)(\w+)', '<a href="http://www.twitter.com/\g<2>/">\g<1>\g<2></a>', value)
    return mark_safe(new_value)
  except:
    return value
    
    
@register.filter
def link_hashtags(value):
  """
  Finds all #hastags and links them to their a Twitter search.

  Example::

    {{ object.quote|link_hashtags }}

  """
  try:
    new_value = re.sub(r'(#)(\w+)', '<a href="http://search.twitter.com/search?q=%23\g<2>">\g<1>\g<2></a>', value)
    return mark_safe(new_value)
  except:
    return value
    

@register.filter
def twitter_links(value):
  """
  Finds all @ mentions and #hastags and links them to Twitter.

  Example::

    {{ object.quote|twitter_links }}

  """
  try:
    new_value = link_hashtags(link_mentions(value))
    return mark_safe(new_value)
  except:
    return value

class GetMostPopularWordsNode(template.Node):
    def __init__(self, num, varname):
      self.num, self.varname = num, varname

    def render(self, context):
        from string import punctuation
        from django.template.defaultfilters import dictsortreversed
        try:
          removelist = ["a", "an", "as", "at", "but", "by", "for", "from",
                        "is", "in", "into", "of", "off", "on", "onto", "per",
                        "since", "than", "the", "this", "that", "to", "up", "via",
                        "with", "and", "it", "be", "was", "i","you","me","my","is","so",
                        "some","it's","its","are","if","some","there", "what","just", ""]
        
          cat_statuses = ""
          for status in Status.objects.all():
            cat_statuses += status.body + " " 
          wordlist = cat_statuses.split()
          punctuation = punctuation.replace('@', '')
          wordlist = [word.strip(punctuation).lower() for word in wordlist]
          wordfreq = [wordlist.count(p) for p in wordlist]
          dictionary = dict(zip(wordlist,wordfreq))
          word_dict_list = []
          for key in dictionary:
            if key not in removelist and not key.startswith('@'):
              word_dict_list.append({ 'name': key, 'count': dictionary[key] })
          context[self.varname] = dictsortreversed(word_dict_list, 'count')[:int(self.num)]
        except:
          pass
        return ''


@register.tag
def get_most_popular_words(parser, token):
    """
    Retrieves the most commonly used words in statuses as stores them in a context variable. Drops common stop words and Twitter user name in the @whatever format.

    Syntax::

        {% get_most_popular_words 20 as [varname] %}

    Example::

        {% get_most_popular_words 20 as word_list %}

    """
    bits = token.contents.split()
    return GetMostPopularWordsNode(bits[1],bits[3])
    
    
class GetMostPopularPeopleNode(template.Node):
    def __init__(self, num, varname):
      self.num, self.varname = num, varname

    def render(self, context):
      from string import punctuation
      from django.template.defaultfilters import dictsortreversed
      try:
        cat_statuses = ""
        for status in Status.objects.all():
          cat_statuses += status.body + " " 
        wordlist = cat_statuses.split()
        punctuation = punctuation.replace('@', '')
        wordlist = [word.strip(punctuation).lower().replace("'s", '') for word in wordlist]
        wordfreq = [wordlist.count(p) for p in wordlist]
        dictionary = dict(zip(wordlist,wordfreq))
        word_dict_list = []
        for key in dictionary:
          if key.startswith('@'):
            word_dict_list.append({ 'name': key[1:], 'count': dictionary[key] })
        context[self.varname] = dictsortreversed(word_dict_list, 'count')[:int(self.num)]
      except:
        pass
      return ''


@register.tag
def get_most_popular_people(parser, token):
    """
    Retrieves the most commonly referred-to people in statuses as stores them in a context variable.

    Syntax::

        {% get_most_popular_people 20 as [varname] %}

    Example::

        {% get_most_popular_people 20 as word_list %}

    """
    bits = token.contents.split()
    return GetMostPopularPeopleNode(bits[1],bits[3])