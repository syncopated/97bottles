import datetime

from django.contrib.auth.models import User

from haystack import indexes
from haystack.sites import site
from tagging.models import Tag

from savoy.contrib.blogs.models import *

from ninetyseven.apps.beers.models import *

class BeerIndex(indexes.SearchIndex):
  text = indexes.CharField(document=True, use_template=True)
  
  def should_update(self, instance):
    """ 
    When certain actions happen, a beer may be saved several times in a row.
    In order to prevent indexing every single time, check the date_updated.
    If it's less than five seconds ago, don't index the beer again.
    """
    return (datetime.datetime.now() - instance.date_updated).seconds > 5
        
class BreweryIndex(indexes.SearchIndex):
  text = indexes.CharField(document=True, use_template=True)
  
  def should_update(self, instance):
    """ 
    When certain actions happen, a brewery may be saved several times in a row.
    In order to prevent indexing every single time, check the date_updated.
    If it's less than five seconds ago, don't index the brewery again.
    """
    return (datetime.datetime.now() - instance.date_updated).seconds > 5
  
class EntryIndex(indexes.SearchIndex):
  text = indexes.CharField(document=True, use_template=True)
    
class UserIndex(indexes.SearchIndex):
  text = indexes.CharField(document=True, use_template=True)
  
  def should_update(self, instance):
    """ Don't index users when they're just logging in. """
    return (datetime.datetime.now() - instance.last_login).seconds > 10
    
class TagIndex(indexes.SearchIndex):
  text = indexes.CharField(document=True, use_template=True)
    
site.register(Beer, BeerIndex)
site.register(Brewery, BreweryIndex)
# site.register(Entry, EntryIndex)
site.register(User, UserIndex)
site.register(Tag, TagIndex)