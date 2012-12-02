import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType

class UserBeerScoreManager(models.Manager):
  def create_or_update(self, instance, **kwargs):
    """
    Create or update a UserBeerScore from some Review or Fave.
    """
    from ninetyseven.apps.beers.models import Beer
    from ninetyseven.apps.reviews.models import Review
    from faves.models import Fave
    
    if hasattr(instance, 'created_by'):
      # This is a review
      user = instance.created_by
      beer = instance.beer
      review = instance
    elif hasattr(instance, 'user'):
      # This is a fave
      user = instance.user
      beer = instance.content_object
      try: review = Review.objects.get(created_by=user, beer=beer)
      except: review = None

    beer_content_type = ContentType.objects.get_for_model(Beer)
    
    try:    favorite = Fave.active_objects.get(type__slug="favorites", user=user, content_type=beer_content_type, object_id=beer.id)
    except: favorite = None
    try:    nasty = Fave.active_objects.get(type__slug="nasty", user=user, content_type=beer_content_type, object_id=beer.id)
    except: nasty = None
    try:    to_drink = Fave.active_objects.get(type__slug="to-dos", user=user, content_type=beer_content_type, object_id=beer.id)
    except: to_drink = None

    if review:      score = int((review.rating+5)/10)*10 # rounded off rating
    elif favorite:  score = 90 # if you said "favorite", you effectively gave it a 90/100
    elif nasty:     score = 10 # if you said "nasty", you effectively gave it a 10/100
    elif to_drink:  score = 70 # if you said "to drink", you effectively gave it a 70/100
    else:           score = 0 # This should never happen, but just in case.
    
    user_beer_score, created = self.get_or_create(
      user = user,
      beer = beer,
      defaults = { 'score': score },
    )
    user_beer_score.score = score
    user_beer_score.save()
    return user_beer_score


class UserInfoManager(models.Manager):
  def create_or_update(self, instance, **kwargs):
    """
    Create or update a UserInfo from some User.
    """
    user_info, created = self.get_or_create(
      user = instance,
    )
    return user_info
  
  def update_contribution_score(self, instance, **kwargs):
    """
    Update the user's contribution score with the new data.
    """
    if instance.created_by:
      user_info = instance.created_by.info
      user_info.save() # Saving updates the contribution score.

class BreweryManager(models.Manager):
  def update_rating(self, instance, **kwargs):
    """
    When a Beer item is saved or deleted, update the Brewery's rating with the new data.
    """
    beer = instance
    if instance.brewery:
      brewery = instance.brewery
      brewery.save() # Saving updates the rating.

class BeerManager(models.Manager):
  def update_rating(self, instance, **kwargs):
    """
    When a Review or Fave item is saved or deleted, update the Beer's rating with the new data.
    """
    try:
      beer = instance.beer
    except AttributeError:
      try:
        beer = instance.content_object
      except AttributeError:
        beer = None
    if beer:
      beer.save() # Saving updates the rating.
  
  def update_characteristics(self, instance, **kwargs):
    """
    When a Review item is saved, update the Beer's characteristics with the new data.
    """
    from django.template.defaultfilters import dictsortreversed
    from ninetyseven.apps.reviews.models import Review
    from tagging.models import Tag
    beer = instance.beer
    reviews = Review.objects.filter(beer=beer)
    tags = Tag.objects.usage_for_queryset(reviews, counts=True)
    top_tags = dictsortreversed(tags, 'count')[:5]
    beer.characteristics = " ".join(tag.name for tag in  top_tags)
    beer.save()
    
  def for_serving_type_in_city(self, serving_type, city, num=10):
    """
    Returns the top "num" beers found in a city, based on serving type.
    This is primary useful for the serving type "On tap." For example, if
    you pass this "On tap" and "Seattle," you'll get the beers which were
    reviewed the most often by people who said they were in Seattle and drank
    the beer from a tap. Effectively, this should be a list of the "num" beers
    you're most likely to find on tap in Seattle.
    """
    from ninetyseven.apps.reviews.models import Review
    from ninetyseven.apps.beers.models import ServingType
    reviews = Review.objects.filter(city=city, serving_type=serving_type)
    
    # Create a dict of the beers in the format { beer_id : review_count }
    beer_dict = {}
    for review in reviews:
      if beer_dict.has_key(review.beer.id):
        count = beer_dict[review.beer.id]
      else:
        count=0
      beer_dict[review.beer.id] = count+1
    
    # Sort the dict by number of reviews (higest first).
    beer_list = sorted(beer_dict.iteritems(), key=lambda (k,v): (v,k), reverse=True)

    # Create a list of beer ids to Query.
    beer_id_list = []
    for beer_id in beer_id_list[:num]:
      beer_id_list.append(beer_id)
    
    # Return a QuerySet of the beers.
    return self.filter(id__in=beer_id_list)
    
  
  def for_variety(self, variety):
    """
    Returns beers for the given variety (a Category instance), 
    regardless of level of depth.
    """
    return self.filter(variety__path__startswith=variety.path)
  
  def similar_characteristics(self, beer, num=10):
    """
    Returns beers with similar characteristics as the beer provided.
    By default, returns 10 beers, but this can be overridden using the
    num argument.
    """
    from tagging.models import TaggedItem
    return TaggedItem.objects.get_related(beer, self, num=num)
    
  def update_top_rated(self, num=10):
    """
    Finds the top [num] beers on the site and checks their "top rated" box,
    unchecking any "top rated" boxes that should no longer be checked. This
    is run after a beer is saved.
    """
    top_beers = self.all().order_by("-rating")[:num]
    top_beers_ids = [ beer.id for beer in top_beers ]
    for beer in top_beers:
      beer.top_rated = True
      beer.save()
    no_longer_top_beers = self.exclude(id__in=top_beers_ids).filter(top_rated=True)
    for beer in no_longer_top_beers:
      beer.top_rated = False
      beer.save()
      print beer
  
  def update_staff_favorites(self, num=10):
    """
    Finds the top [num] beers as rated by staff and checks their "staff favorite"
    box, unchecking any "staff favorite" boxes that should no longer be checked. This
    is run after a beer is saved.
    """
    staff_favorite_beers = self.all().order_by("-rating_by_staff")[:num]
    staff_favorite_ids = [ beer.id for beer in staff_favorite_beers ]
    for beer in staff_favorite_beers:
      beer.staff_favorite = True
      beer.save()
    no_longer_staff_favorite_beers = self.filter(staff_favorite=True)
    for beer in no_longer_staff_favorite_beers:
      if beer.id not in staff_favorite_ids:
        beer.staff_favorite = False
        beer.save()
      
  def update_womens_favorites(self, num=10):
    """
    Finds the top [num] beers as rated by women and checks their "womens favorite"
    box, unchecking any "womens favorite" boxes that should no longer be checked. This
    is run after a beer is saved.
    """
    womens_favorite_beers = self.all().order_by("-rating_by_women")[:num]
    womens_favorite_ids = [ beer.id for beer in womens_favorite_beers ]
    for beer in womens_favorite_beers:
      beer.womens_favorite = True
      beer.save()
    no_longer_womens_favorite_beers = self.exclude(id__in=womens_favorite_ids).filter(womens_favorite=True)
    for beer in no_longer_womens_favorite_beers:
      beer.womens_favorite = False
      beer.save()
      
  def update_mens_favorites(self, num=10):
    """
    Finds the top [num] beers as rated by women and checks their "womens favorite"
    box, unchecking any "womens favorite" boxes that should no longer be checked. This
    is run after a beer is saved.
    """
    mens_favorite_beers = self.all().order_by("-rating_by_men")[:num]
    mens_favorite_ids = [ beer.id for beer in mens_favorite_beers ]
    for beer in mens_favorite_beers:
      beer.mens_favorite = True
      beer.save()
    no_longer_mens_favorite_beers = self.exclude(id__in=mens_favorite_ids).filter(mens_favorite=True)
    for beer in no_longer_mens_favorite_beers:
      beer.mens_favorite = False
      beer.save()
      
      
class SkunkyBeerManager(models.Manager):
  """
  Custom manager for beers which only returns beers that have a rating of 20 or lower.
  """
  def get_query_set(self):
    return super(SkunkyBeerManager, self).get_query_set().filter(rating__lte=20).order_by('rating')
    
class GirlieBeerManager(models.Manager):
  """
  Custom manager for beers which only returns beers that have a rating of 80 or higher by women.
  """
  def get_query_set(self):
    return super(GirlieBeerManager, self).get_query_set().filter(rating_by_women__gte=80).order_by('-rating_by_women')
    
class HighRatedBeerManager(models.Manager):
  """
  Custom manager for beers which only returns beers that have a rating of 90 or higher.
  """
  def get_query_set(self):
    return super(HighRatedBeerManager, self).get_query_set().filter(rating__gte=90).order_by('-rating')
    
class StaffPickBeerManager(models.Manager):
  """
  Custom manager for beers which only returns beers that have a rating of 80 or higher by staff.
  """
  def get_query_set(self):
    return super(StaffPickBeerManager, self).get_query_set().filter(staff_favorite=True).order_by('-rating_by_staff')
    
class HighAlcoholBeerManager(models.Manager):
  """
  Custom manager for beers which only returns beers that have a ABV of 10% or higher.
  """
  def get_query_set(self):
    return super(HighAlcoholBeerManager, self).get_query_set().filter(alcohol_by_volume__gte=10).order_by('-alcohol_by_volume')
    
class HoppyBeerManager(models.Manager):
  """
  Custom manager for beers which only returns beers that have a IBU of 70 or higher.
  """
  def get_query_set(self):
    return super(HoppyBeerManager, self).get_query_set().filter(ibu__gte=70).order_by('-ibu')
    
class SessionBeerManager(models.Manager):
  """
  Custom manager for beers which only returns beers that have an ABV of 5 or lower.
  """
  def get_query_set(self):
    return super(SessionBeerManager, self).get_query_set().filter(alcohol_by_volume__lte=5).order_by('alcohol_by_volume')