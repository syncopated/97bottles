from django.db import models
from django.db.models import signals, permalink
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.core.cache import cache
from django.template.defaultfilters import slugify
from operator import add

from tagging.fields import TagField
from tagging.models import TaggedItem, Tag
from categorization.models import Category
from faves.models import Fave

from savoy.core.geo.models import City, GeolocatedItem
from savoy.core.slugs import get_unique_slug_value

from ninetyseven.apps import BaseModel
from ninetyseven.apps.beers.managers import *
from ninetyseven.apps.recommender.models import Recommender

class UserBeerScore(models.Model):
  """
  A UserBeer score is a user's score for a given beer, for use in the recommendation engine.
  """
  user      = models.ForeignKey(User, related_name="scores")
  beer      = models.ForeignKey('Beer', related_name="scores")
  score     = models.IntegerField()
  objects   = UserBeerScoreManager()

  def __unicode__(self):
    return "%s: %s on %s" % (self.user.username, self.score, self.beer.name)


class UserInfo(models.Model):
  """
  A profile of a user's activity and recommendations on 97 Bottles.
  """
  user                  = models.OneToOneField(User, primary_key=True, related_name="info")
  contribution_score    = models.IntegerField(blank=True, null=True)
  objects               = UserInfoManager()
  
  def _calculate_contribution_score(self):
    """
    Adds a contribution score for this user, and then returns self.
    Higher scores mean the user has contributed more.
    """
    score = 0
    for review in self.user.review_created.all(): 
      if review.comment:
        score = score + 3
      else:
        score = score + 1
    for beer in self.user.beer_created.all(): score = score + 5
    for brewery in self.user.brewery_created.all(): score = score + 2
    for fave in self.user.faves.all(): score = score + 1
    self.contribution_score = score
    return self
    
  
  def highest_rated_breweries_near(self, radius_miles=100):
    """
    Returns a list of breweries within the given radius, ordered by rating (highest_first).
    """
    if self.user.profile.city:
      from django.contrib.contenttypes.models import ContentType
      content_type = ContentType.objects.get_for_model(Brewery)
      nearby_brewery_geo_items = self.user.profile.city.location().get_geolocated_items_within_radius(radius_miles=radius_miles, content_type=content_type)
      brewery_ids = [ item.object_id for item in nearby_brewery_geo_items ]
      return Brewery.objects.filter(id__in=brewery_ids).order_by('-rating')
    else:
      return None
  
  def highest_rated_beers_near(self, radius_miles=100):
    """
    Returns a list of beers that have been drank within the given radius, ordered by rating (highest_first).
    """
    if self.user.profile.city:
      from django.contrib.contenttypes.models import ContentType
      content_type = ContentType.objects.get_for_model(Review)
      nearby_review_geo_items = self.user.profile.city.location().get_geolocated_items_within_radius(radius_miles=radius_miles, content_type=content_type)
      review_ids = [ item.object_id for item in nearby_review_geo_items ]
      reviews =  Review.objects.filter(id__in=review_ids)
      beer_ids = [ review.beer.id for review in reviews ]
      return Beer.objects.filter(id__in=beer_ids).order_by('-rating').distinct()
    else:
      return None
  
  def incoming_user_recommendations(self):
    """
    Returns a list of user recommendations that have not been dismissed for this user.
    """
    UserRecommendation = models.get_model("beers","userrecommendation")
    return UserRecommendation.objects.filter(dismissed=False, to_user=self.user)
  
  def recommended_beers(self, values=False):
    """
    Returns a list of recommended beers for this user, combining all the possible recommendation methods.
    """
    recommended_beers =  map(lambda *t: filter(lambda x: x is not None,t),self.recommended_beers_by_users(),self.recommended_beers_by_tags())
    recs = []
    for item in recommended_beers:
      for beer in item:
        recs.append(beer)
    return recs
  
  def recommended_beers_by_users(self, values=False):
    """
    Returns a cached list of recommended beers for this user, based on similarity matrix with other users.
    """
    # UNCACHED VERSION.
    # if values:
    #   return Recommender.objects.get_best_items_for_user(self.user, User.objects.all(), Beer.objects.filter(rating__isnull=False))
    # else:
    #   return [ item[1] for item in Recommender.objects.get_best_items_for_user(self.user, User.objects.all(), Beer.objects.filter(rating__isnull=False))]
    
    # CACHED VERSION.
    cache_key = slugify(u'recommended_beers_by_users_%s' % self.__unicode__())
    recommended_beers_by_users = cache.get(cache_key)
    if recommended_beers_by_users == []:
      return recommended_beers_by_users
    if not recommended_beers_by_users:
      recommended_beers_by_users = Recommender.objects.get_best_items_for_user(self.user, User.objects.all(), Beer.objects.filter(rating__isnull=False))
      cache.add(cache_key, recommended_beers_by_users, 7200)
    if values:
      return recommended_beers_by_users
    else:
      faves_list = [ fave.content_object for fave in Fave.active_objects.filter(user=self.user) ]
      return [ item[1] for item in recommended_beers_by_users if item[1] not in faves_list ]
  
  def similar_users(self, values=False):
    """
    Returns a cached list of similar users for this user.
    """
    # UNCACHED VERSION
    # if values:
    #   Recommender.objects.get_similar_users(self.user, User.objects.all(), Beer.objects.filter(rating__isnull=False))
    # else:
    #   return [ item[1] for item in Recommender.objects.get_similar_users(self.user, User.objects.all(), Beer.objects.filter(rating__isnull=False))]
    
    # CACHED VERSION.
    cache_key = slugify(u'similar_users_%s' % self.__unicode__())
    similar_users = cache.get(cache_key)
    if similar_users == []:
      return similar_users
    if not similar_users:
      similar_users = Recommender.objects.get_similar_users(self.user, User.objects.all(), Beer.objects.filter(rating__isnull=False))
      cache.add(cache_key, similar_users, 7200)
      similar_users = cache.get(cache_key)
    if values:
      return similar_users
    else:
      return [ item[1] for item in similar_users ]
  
  def recommended_beers_by_tags(self, values=False):
    """
    Returns a cached list of recommended beers, based on tags. 
    """
    # UNCACHED VERSION
    # if values:
    #   return Recommender.objects.get_content_based_recs(self.user, Beer.objects.filter(rating__isnull=False))
    # else:
    #   return [ item[1] for item in Recommender.objects.get_content_based_recs(self.user, Beer.objects.filter(rating__isnull=False))]
    
    # CACHED VERSION.
    cache_key = slugify(u'recommended_beers_by_tags_%s' % self.__unicode__())
    recommended_beers_by_tags = cache.get(cache_key)
    if recommended_beers_by_tags == []:
      return recommended_beers_by_tags
    if not recommended_beers_by_tags:
      recommended_beers_by_tags = Recommender.objects.get_content_based_recs(self.user, Beer.objects.filter(rating__isnull=False))
      cache.add(cache_key, recommended_beers_by_tags, 7200)
      recommended_beers_by_tags = cache.get(cache_key)
    if values:
      return recommended_beers_by_tags
    else:
      faves_list = [ fave.content_object for fave in Fave.active_objects.filter(user=self.user) ]
      return [ item[1] for item in recommended_beers_by_tags if item[1] not in faves_list ]
  
  def favorite_varieties(self):
    """
    An algorithmically generated list of a user's favorite beer categories.
    """
    cache_key = slugify(u'favorite_varieties_%s' % self.__unicode__())
    favorite_varieties = cache.get(cache_key)
    if favorite_varieties == []:
      return favorite_varieties
    if not favorite_varieties:
      faves               = self.user.faves.filter(withdrawn=False)
      reviews             = self.user.review_created.all()
      varieties           = Category.objects.all()
      favorite_varieties  = {}
      for fave in faves:
        if not favorite_varieties.has_key(fave.content_object.variety): favorite_varieties[fave.content_object.variety] = 5
        favorite_varieties[fave.content_object.variety] = favorite_varieties[fave.content_object.variety] + 5
      for review in reviews:
        if not favorite_varieties.has_key(review.beer.variety): favorite_varieties[review.beer.variety] = 1
        if review.rating > 80: favorite_varieties[review.beer.variety] = favorite_varieties[review.beer.variety] + 5
        elif review.rating > 60: favorite_varieties[review.beer.variety] = favorite_varieties[review.beer.variety] + 4
        elif review.rating > 40: favorite_varieties[review.beer.variety] = favorite_varieties[review.beer.variety] + 3
        elif review.rating > 20: favorite_varieties[review.beer.variety] = favorite_varieties[review.beer.variety] + 2
        else: favorite_varieties[review.beer.variety] = favorite_varieties[review.beer.variety] + 1
      items = [(value, key) for key, value in favorite_varieties.items()]
      items.sort(reverse=True)
      cache.add(cache_key, [ item[1] for item in items], 28800)
      favorite_varieties = cache.get(cache_key)
    return favorite_varieties

  def __unicode__(self):
    return self.user.username

  def save(self, force_insert=False, force_update=False):
    """
    Update denormalized fields, then save the object.
    """
    self._calculate_contribution_score()
    super(UserInfo, self).save(force_insert=force_insert, force_update=force_update)

class Vessel(BaseModel):
  """
  A Vessel is an object from which you drink beer (i.e. bottle, 
  pint glass, goblet, stein, can, etc.)
  """
  name              = models.CharField(max_length=255, help_text="The name of a vessel, such as 'Stein', 'Mug', 'Bottle', 'Pint glass', etc.")
  slug              = models.SlugField(help_text="A URL-friendly version of the name. Auto-populated.")
  
  def __unicode__(self):
    return u"%s" % self.name

class ServingType(BaseModel):
  """
  A ServingType is method in which beer is served (from the tap, from a keg, poured from bottle, etc.)
  """
  name              = models.CharField(max_length=255, help_text="The name of a type, such as 'From the tap', 'From a keg', etc.")
  slug              = models.SlugField(help_text="A URL-friendly version of the name. Auto-populated.")

  def __unicode__(self):
    return u"%s" % self.name

class VesselImage(models.Model):
  """
  A VesselImage is an image depicting a vessel in a particular beer color.
  """
  vessel            = models.ForeignKey(Vessel)
  color             = models.ForeignKey('BeerColor', blank=True, null=True)
  image             = models.ImageField(upload_to="img/vessel_images")
  
  def __unicode__(self):
    return u"%s: %s" % (self.vessel, self.color)

class BreweryType(models.Model):
  """
  A BreweryType is a particular type of brewery.
  """
  name              = models.CharField(max_length=255, help_text="The name of a brewery type, such as 'Microbrew', 'Homebrew', etc.")
  slug              = models.SlugField(help_text="A URL-friendly version of the name. Auto-populated.")

  def __unicode__(self):
    return self.name

class Brewery(BaseModel):
  """
  A brewery is a place where beer is brewed.
  """
  name              = models.CharField(max_length=255, db_index=True, help_text="The name of a particular brewery, such as 'Free State Brewing Co.'.")
  slug              = models.SlugField(help_text="A URL-friendly version of the name. Auto-populated.")
  type              = models.ForeignKey(BreweryType, blank=True, null=True, help_text="The type of brewery this is.")
  city              = models.ForeignKey(City, blank=True, null=True, related_name="breweries", help_text="The city this brewery is located in.")
  url               = models.URLField(blank=True, verify_exists=True, help_text="The URL to this brewery's web site.")
  rating            = models.PositiveIntegerField(blank=True, null=True, editable=False)
  
  objects           = BreweryManager()
  
  class Meta:
    verbose_name_plural = "Breweries"
    ordering = ('name',)
  
  def __unicode__(self):
    return self.name
  
  @permalink
  def get_absolute_url(self):
    """
    Returns the URL for this Brewery's page on the site.
    """
    if self.city.country == "us":
      return ('brewery_detail', None, {'country': slugify(self.city.country), 'state': slugify(self.city.state), 'city': slugify(self.city.city), 'brewery_slug': self.slug})
    else:
      if self.city.province:
        return ('brewery_detail', None, {'country': slugify(self.city.country), 'state': slugify(self.city.province), 'city': slugify(self.city.city), 'brewery_slug': self.slug})
      else:
        return ('city_detail', None, {'country': slugify(self.city.country), 'state': slugify(self.city.city), 'city': self.slug})
    return
    
  def _update_rating(self):
    """
    Updates the rating for this brewery, and then returns it.
    """
    ratings = [beer.rating for beer in self.beers.all() if beer.rating != None]
    if len(ratings) > 0:
      self.rating = reduce(add, ratings) / len(ratings)
    else:
      self.rating = None
    return self
  
  def _serialize(self):
    obj = {
      "id": self.pk,
      "name": self.name,
      "url": 'http://97bottles.com%s' % self.get_absolute_url(),
      "rating": self.rating,
      "type": getattr(self, 'type.name', None),
      "city": {
        "id": self.city.id,
        "name": self.city.city,
        "state": self.city.state,
        "province": self.city.province,
        "country": self.city.country,
      },
    }
    return obj
  
  def save(self, force_insert=False, force_update=False):
    """
    Create the slug, then save the Brewery and a Geo item.
    """
    from django.template.defaultfilters import slugify
    if not self.slug:
      self.slug = get_unique_slug_value(Brewery, slugify(self.name))
    self._update_rating()
    super(Brewery, self).save(force_insert=force_insert, force_update=force_update)
    if self.city.location():
      GeolocatedItem.objects.create_or_update(self, location=(self.city.location().latitude, self.city.location().longitude), city=self.city)

class BeerColor(models.Model):
  """
  A BeerColor is a particular color of beer.
  """
  srm = models.IntegerField(help_text="The SRM/Lovibond value of this color.")
  ebc = models.IntegerField(help_text="The EBC value of this color.")
  example = models.CharField(max_length=255)
  color = models.CharField(max_length=7, help_text="The hex value of this color, i.e. '#bc610b.'")
  
  class Meta:
    ordering = ('srm',)
  
  @property
  def lovibond(self):
    return self.srm
  
  def __unicode__(self):
    if self.example:
      return u'%s (%s)' % (self.srm, self.example)
    else:
      return u'%s' % self.srm

class Batch(models.Model):
  """
  A Batch is a particular batch of beer, such as "Winter Seasonal".
  """
  name              = models.CharField(max_length=255, help_text="The name of a batch, such as 'Winter Seasonal', 'Special Release', etc.")
  slug              = models.SlugField(help_text="A URL-friendly version of the name. Auto-populated.")

  class Meta:
    verbose_name_plural = "Batches"
    
  def __unicode__(self):
    return self.name

class Beer(BaseModel):
  """
  A Beer is a particular brew of beer.
  """
  name              = models.CharField(max_length=255, db_index=True, help_text="The name of a brew, such as 'Ad Astra Ale' or 'Oatmeal Stout'. If the name is generic, like 'Oatmeal Stout', be sure to include the brewery name. Ex. 'Barney Flats Oatmeal Stout'.")
  slug              = models.SlugField(help_text="A URL-friendly version of the name. Auto-populated.")
  brewery           = models.ForeignKey(Brewery, related_name="beers", help_text="The brewery responsible for this beer.")
  variety           = models.ForeignKey(Category, null=True, related_name="beers", help_text="The variety of beer, such as 'American Ale', or 'Lager'.")
  alcohol_by_volume = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Format: 7.5% should be entered as '7.5'.")
  alcohol_by_weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Format: 9.25% should be entered as '9.25'.")
  ibu               = models.IntegerField(blank=True, null=True, help_text="International Bitterness Units. Enter a number between 1 and 100.")
  preferred_vessel  = models.ForeignKey(Vessel, blank=True, null=True, related_name="beers_preferred_by", help_text="The vessel this beer is typically served in.")
  characteristics   = TagField(blank=True, null=True, help_text="Tags defining the characteristics of this beer, including color and taste words like 'nutty','bitter', and 'brown'. Separate tags with spaces or commas.")
  color             = models.ForeignKey(BeerColor, blank=True, null=True, help_text="The color of this beer.")
  batch             = models.ForeignKey(Batch, blank=True, null=True, help_text="The batch that begat this beer.")
  description       = models.TextField(blank=True, help_text="An objective, written description of this beer, such as one from the brewery itself. No heartfelt opinions allowed!")
  rating            = models.PositiveIntegerField(blank=True, null=True, editable=False)
  rating_by_women   = models.PositiveIntegerField(blank=True, null=True, editable=False)
  womens_favorite   = models.BooleanField(default=False)
  rating_by_men     = models.PositiveIntegerField(blank=True, null=True, editable=False)
  mens_favorite     = models.BooleanField(default=False)
  rating_by_staff   = models.PositiveIntegerField(blank=True, null=True, editable=False)
  staff_favorite    = models.BooleanField(default=False)
  top_rated         = models.BooleanField(default=False)
  interestingness   = models.PositiveIntegerField(blank=True, null=True, editable=False)
  faves             = generic.GenericRelation(Fave)
  
  objects           = BeerManager()
  skunky            = SkunkyBeerManager()
  girlie            = GirlieBeerManager()
  high_rated        = HighRatedBeerManager()
  staff_pick        = StaffPickBeerManager()
  high_alcohol      = HighAlcoholBeerManager()
  hoppy             = HoppyBeerManager()
  session           = SessionBeerManager()
  
  def __unicode__(self):
    return u"%s, %s" % (self.name, self.brewery)
  
  @models.permalink
  def get_absolute_url(self):
    """
    Returns the URL to the detail page for this beer.
    """
    if self.brewery.city.country == "us":
      return ('beer_detail', None, {'country': slugify(self.brewery.city.country), 'state': slugify(self.brewery.city.state), 'city': slugify(self.brewery.city.city), 'brewery_slug': self.brewery.slug, 'slug': self.slug })
    else:
      if self.brewery.city.province:
        return ('beer_detail', None, {'country': slugify(self.brewery.city.country), 'state': slugify(self.brewery.city.province), 'city': slugify(self.brewery.city.city), 'brewery_slug': self.brewery.slug, 'slug': self.slug })
      else:
        return ('beer_detail', None, {'country': slugify(self.brewery.city.country), 'state': None, 'city': slugify(self.brewery.city.city), 'brewery_slug': self.brewery.slug, 'slug': self.slug })
    return

  def vessel_image(self):
    """
    Returns the VesselImage object appropriate for this beer, based on it's color and preferred_vessel.
    """
    vessel_image = VesselImage.objects.get(vessel__slug="pint-glass", color=BeerColor.objects.get(srm=13))
    if self.color and self.preferred_vessel:
      try: vessel_image = VesselImage.objects.get(color=self.color, vessel=self.preferred_vessel)
      except: pass
    elif self.color and not self.preferred_vessel:
      try: vessel_image = VesselImage.objects.get(vessel__slug="pint-glass", color=self.color)
      except: pass
    elif self.preferred_vessel and not self.color:
      try: vessel_image = VesselImage.objects.get(vessel=self.preferred_vessel, color=None)
      except: pass
    elif not self.color and not self.preferred_vessel:
      try: vessel_image = VesselImage.objects.get(vessel__slug="pint-glass", color=None)
      except: pass
    return vessel_image

  def is_skunky(self):
    return self in Beer.skunky.all()
  
  def is_girlie(self):
    return self in Beer.girlie.all()
    
  def is_high_rated(self):
    return self in Beer.high_rated.all()
    
  def is_staff_pick(self):
    return self in Beer.staff_pick.all()
    
  def is_high_alcohol(self):
    return self in Beer.high_alcohol.all()

  def is_bitter(self):
    return self in Beer.bitter.all()
  
  def sections(self):
    """
    Returns a QuerySet of sections that contain this beer.
    """
    from savoy.contrib.sections.models import Section
    return Section.objects.filter(tags__in=[ tag.id for tag in Tag.objects.get_for_object(self) ])
  
  def cities_drank_in_values(self):
    """
    Returns a list of dicts representing the cities this beer has been drank in,
    based on reviews, along with the number of reviews in each city.
    """
    values = []
    for city in self.cities_drank_in():
      review_count = Review.objects.filter(beer=self, city=city).count()
      city_dict = { 'city': city, 'count': review_count }
      values.append(city_dict)
    return values
  
  def cities_drank_in(self):
    """
    Returns a QuerySet of the cities this beer has been drank in, based on
    the related Review objects.
    """
    return City.objects.filter(reviews__beer=self).distinct()
  
  def other_beers_by_brewery(self):
    """
    Returns other beers by the brewery related to this beer.
    """
    # UNCACHED VERSION
    # return Beer.objects.filter(brewery=self.brewery).exclude(id=self.id)
    
    # CACHED VERSION.
    cache_key = slugify(u'other_beers_by_brewery_%s' % self.slug)
    other_beers_by_brewery = cache.get(cache_key)
    if other_beers_by_brewery == []:
      return other_beers_by_brewery
    if not other_beers_by_brewery:
      cache.add(cache_key, Beer.objects.filter(brewery=self.brewery).exclude(id=self.id), 7200)
      other_beers_by_brewery = cache.get(cache_key)
    return other_beers_by_brewery
  
  def recommended_for_users(self):
    """
    Returns a cached list of users that this beer is recommended for.
    """
    # UNCACHED VERSION
    # if self.rating:
    #   return Recommender.objects.get_best_users_for_item(self, User.objects.all(), Beer.objects.filter(rating__isnull=False))
    # else:
    #   return []
    
    # CACHED VERSION.
    if self.rating:
      cache_key = slugify(u'recommended_for_users_%s' % self.slug)
      recommended_for_users = cache.get(cache_key)
      if recommended_for_users == []:
        return recommended_for_users
      if not recommended_for_users:
        cache.add(cache_key, Recommender.objects.get_best_users_for_item(self, User.objects.all(), Beer.objects.filter(rating__isnull=False)), 7200)
        recommended_for_users = cache.get(cache_key)
      return recommended_for_users
    else:
      return []

  def similar_beers_by_reviews(self):
    """
    Returns a cached list of beers similar to this one, based on reviews.
    i.e. "People who liked this beer also liked..."
    """
    # UNCACHED VERSION
    # if self.rating:
    #   return [recommendation[1] for recommendation in Recommender.objects.get_similar_items(self, User.objects.all(), Beer.objects.filter(rating__isnull=False))]
    # else:
    #   return []
    
    # CACHED VERSION.
    if self.rating:
      cache_key = slugify(u'similar_beers_by_reviews_%s' % self.slug)
      similar_beers_by_reviews = cache.get(cache_key)
      if similar_beers_by_reviews == []:
        return similar_beers_by_reviews
      if not similar_beers_by_reviews:
        cache.add(cache_key, [recommendation[1] for recommendation in Recommender.objects.get_similar_items(self, User.objects.all(), Beer.objects.filter(rating__isnull=False))], 7200)
        similar_beers_by_reviews = cache.get(cache_key)
      return similar_beers_by_reviews
    else:
      return []
    
  def similar_beers_by_tags(self):
    """
    Returns a list of beers similar to this one, based on tags.
    """
    # UNCACHED VERSION
    # if self.rating:
    #   return TaggedItem.objects.get_related(self, Beer, num=None)
    # else:
    #   return []
    
    # CACHED VERSION 
    if self.rating:
      cache_key = slugify(u'similar_beers_by_tags_%s' % self.slug)
      similar_beers_by_tags = cache.get(cache_key)
      if similar_beers_by_tags == []:
        return similar_beers_by_tags
      if not similar_beers_by_tags:
        cache.add(cache_key, TaggedItem.objects.get_related(self, Beer, num=None), 7200)
        similar_beers_by_tags = cache.get(cache_key)
      return similar_beers_by_tags
    else:
      return []
      
  def _calculate_interestingness(self):
    """
    Calculates a numerical score that represents how "interesting" this beer is,
    based on several factors, including its rating, the number of people who
    have reviewed, the number of faves attached to it, and more. Returns the beer,
    with the score value inserted into the interestingness field.
    """
    score = 0
    now = datetime.datetime.now()
    reviews = self.reviews.all()
    faves = self.faves.all()
    if reviews:
      latest_review = self.reviews.latest()
    
    # Add points for this beer's rating. We'll take it's rating times three.
    if self.rating:
      score += self.rating * 3
    
    # Add points for recency of this beer's creation
    # Beers from today get 40 points, from the last seven days
    # gets 36 points, and it goes down from there.
    if self.date_created >= now - datetime.timedelta(days=1): score += 40
    elif self.date_created >= now - datetime.timedelta(days=7): score += 36
    elif self.date_created >= now - datetime.timedelta(days=30): score += 32
    elif self.date_created >= now - datetime.timedelta(days=90): score += 28
    elif self.date_created >= now - datetime.timedelta(days=180): score += 24
    elif self.date_created >= now - datetime.timedelta(days=365): score += 20
    elif self.date_created >= now - datetime.timedelta(days=730): score += 16
    elif self.date_created >= now - datetime.timedelta(days=1095): score += 12
    elif self.date_created >= now - datetime.timedelta(days=1460): score += 8
    elif self.date_created <= now - datetime.timedelta(days=1460): score += 4
      
    # Add points for more recently added reviews of this beer
    # Beers that have reviews today get 40 points, reviews in the
    # last seven days gets 36 points, and it goes down from there.
    if reviews:
      if latest_review.date_created >= now - datetime.timedelta(days=1): score += 40
      elif latest_review.date_created >= now - datetime.timedelta(days=7): score += 36
      elif latest_review.date_created >= now - datetime.timedelta(days=30): score += 32
      elif latest_review.date_created >= now - datetime.timedelta(days=90): score += 28
      elif latest_review.date_created >= now - datetime.timedelta(days=180): score += 24
      elif latest_review.date_created >= now - datetime.timedelta(days=365): score += 20
      elif latest_review.date_created >= now - datetime.timedelta(days=730): score += 16
      elif latest_review.date_created >= now - datetime.timedelta(days=1095): score += 12
      elif latest_review.date_created >= now - datetime.timedelta(days=1460): score += 8
      elif latest_review.date_created <= now - datetime.timedelta(days=1460): score += 4
    
    # Add 40 points for each review of this beer
    if reviews:
      score += reviews.count() * 40
    
    # Add 40 points for each fave of this beer
    if faves:
      score += faves.count() * 40
    
    self.interestingness = score
    return self
    
  
  def _calculate_alcohol(self):
    """
    Given one of either alcohol by weight or alcohol by volume, calculates the other and returns the object.
    """
    from decimal import Decimal
    if self.alcohol_by_volume and not self.alcohol_by_weight:
      self.alcohol_by_weight = self.alcohol_by_volume * Decimal('.8')
    if self.alcohol_by_weight and not self.alcohol_by_volume:
      self.alcohol_by_volume = self.alcohol_by_weight * Decimal('1.25')
    return self
  
  def _update_rating(self):
    """
    Updates the rating for this beer, and then returns it.
    """
    ratings = [review.rating for review in self.reviews.all() if review.rating != None]
    if len(ratings) > 2:
      self.rating = reduce(add, ratings) / len(ratings)
    else:
      self.rating = None
    return self
  
  def _update_preferred_vessel(self):
    """
    Updates the preferred_vessel for this beer, and then returns it.
    """
    vessels = [review.vessel for review in self.reviews.all() if review.vessel != None]
    if len(vessels) > 0:
      results = {}
      for vessel in vessels:
        results[vessel] = results.get(vessel, 0) + 1
      counts = [(j,i) for i,j in results.items()]
      count, top_vessel = max(counts)
      self.preferred_vessel = top_vessel
    else:
      self.preferred_vessel = None
    return self
  
  def _update_rating_by_women(self):
    """
    Updates the rating_by_women for this beer, then returns it.
    """
    ratings = [review.rating for review in self.reviews.filter(created_by__profile__gender=2) if review.rating != None]
    if len(ratings) > 1:
      self.rating_by_women = reduce(add, ratings) / len(ratings)
    else:
      self.rating_by_women = None
    return self
  
  def _update_rating_by_men(self):
    """
    Updates the rating_by_women for this beer, then returns it.
    """
    ratings = [review.rating for review in self.reviews.filter(created_by__profile__gender=1) if review.rating != None]
    if len(ratings) > 0:
      self.rating_by_men = reduce(add, ratings) / len(ratings)
    else:
      self.rating_by_men = None
    return self
    
  def _update_rating_by_staff(self):
    """
    Updates the rating_by_staff for this beer, then returns it.
    """
    ratings = [review.rating for review in self.reviews.filter(created_by__is_staff=True) if review.rating != None]
    if len(ratings) > 0:
      self.rating_by_staff = reduce(add, ratings) / len(ratings)
    else:
      self.rating_by_staff = None
    return self
  
  def _serialize(self):
    obj = {
      "id": self.pk,
      "name": self.name,
      "url": 'http://97bottles.com%s' % self.get_absolute_url(),
      "rating": self.rating,
      "alcohol_by_volume": self.alcohol_by_volume,
      "alcohol_by_weight": self.alcohol_by_weight,
      "ibu": self.ibu,
      "description": self.description,
      "batch": getattr(getattr(self, 'batch', None), 'name', None),
      "preferred_vessel": getattr(getattr(self, 'preferred_vessel', None), 'name', None),
      "characteristics": [ tag.name for tag in Tag.objects.get_for_object(self) ],
      "color": {
        "lovibond": getattr(getattr(self, 'color', None), 'lovibond', None),
        "ebc":  getattr(getattr(self, 'color', None), 'ebc', None),
        "hex":  getattr(getattr(self, 'color', None), 'hex', None),
        "example":  getattr(getattr(self, 'color', None), 'example', None),
      },
      "variety": {
        "name": getattr(getattr(self, 'variety', None), 'name', None),
        "path": getattr(getattr(self, 'variety', None), 'path', None),
        "url": 'http://97bottles.com/%s/' % getattr(getattr(self, 'variety', None), 'path', None),
        "description": getattr(getattr(self, 'variety', None), 'description', None),
      },
      "brewery": {
        "id": self.brewery.id,
        "name": self.brewery.name,
        "url": "http://97bottles.com%s" % self.brewery.get_absolute_url(),
        "rating": self.brewery.rating,
        "city": {
          "id": getattr(getattr(getattr(self, 'brewery', None), 'city', None), 'id', None),
          "name": getattr(getattr(getattr(self, 'brewery', None), 'city', None), 'city', None),
          "state": getattr(getattr(getattr(self, 'brewery', None), 'city', None), 'state', None),
          "province": getattr(getattr(getattr(self, 'brewery', None), 'city', None), 'province', None),
          "country": getattr(getattr(getattr(self, 'brewery', None), 'city', None), 'country', None),
        },
      },
    }
    return obj

  
  def save(self, force_insert=False, force_update=False):
    """
    Calculate the ABV and ABW if possible, create the slug, update some counts, then save the beer.
    """
    from django.template.defaultfilters import slugify
    if not self.slug:
      self.slug = get_unique_slug_value(Beer, slugify(self.name))
    self._calculate_alcohol()
    self._calculate_interestingness()
    self._update_rating()
    self._update_rating_by_men()
    self._update_rating_by_women()
    self._update_rating_by_staff()
    self._update_preferred_vessel()
    super(Beer, self).save(force_insert=force_insert, force_update=force_update)


class UserRecommendation(models.Model):
  """ A UserRecommendation is a recommendation of a beer from one user to another. """
  beer          = models.ForeignKey(Beer, related_name="user_recommendations")
  from_user     = models.ForeignKey(User, related_name="user_recommendations_sent")
  to_user       = models.ForeignKey(User, related_name="user_recommendations_received")
  date_created  = models.DateTimeField(auto_now_add=True)
  dismissed     = models.BooleanField(default=False)
  
  def __unicode__(self):
    return u"%s: Recommended to %s by %s" % (self.beer.name, self.to_user.username, self.from_user.username)

Review = models.get_model("reviews", "review")

# When a user is saved, create or update a user info object.
signals.post_save.connect(UserInfo.objects.create_or_update, sender=User)

# When a fave is saved, update the beer's rating.
# Also update the user's score for the beer.
signals.post_save.connect(Beer.objects.update_rating, sender=Fave)
signals.post_save.connect(UserBeerScore.objects.create_or_update, sender=Fave)

# When a review is saved, update the beer's rating and characteristics.
# Also update the user's contribution score.
# Also update the user's score for the beer.
signals.post_save.connect(Beer.objects.update_rating, sender=Review)
signals.post_save.connect(Beer.objects.update_characteristics, sender=Review)
signals.post_save.connect(UserInfo.objects.update_contribution_score, sender=Review)
signals.post_save.connect(UserBeerScore.objects.create_or_update, sender=Review)

# When a review is deleted, update the beer's rating.
# Also update the user's contribution score.
signals.post_delete.connect(Beer.objects.update_rating, sender=Review)
signals.post_delete.connect(UserInfo.objects.update_contribution_score, sender=Review)

# When a beer is saved, update the brewery's rating.
# Also update the user's contribution score.
# Also update the awards.
signals.post_save.connect(Brewery.objects.update_rating, sender=Beer)
signals.post_save.connect(UserInfo.objects.update_contribution_score, sender=Beer)

# When a beer is deleted, update the brewery's rating.
# Also update the user's contribution score.
signals.post_delete.connect(Brewery.objects.update_rating, sender=Beer)
signals.post_delete.connect(UserInfo.objects.update_contribution_score, sender=Beer)

# When a brewery is saved, update the user's contribution score.
signals.post_save.connect(UserInfo.objects.update_contribution_score, sender=Brewery)

# When a brewery is deleted, update the user's contribution score.
signals.post_delete.connect(UserInfo.objects.update_contribution_score, sender=Brewery)