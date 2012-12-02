from django.contrib.sites.models import Site
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from piston.handler import BaseHandler, AnonymousBaseHandler
from piston.utils import rc
from tagging.models import Tag
from faves.models import *

from ninetyseven.apps.beers.models import *

site = Site.objects.get(id=settings.SITE_ID)
site_url = "http://%s" % site.domain

class AnonymousBeerHandler(AnonymousBaseHandler):
  model = Beer
  fields = (
    'id', 
    'name', 
    'url', 
    'rating', 
    'alcohol_by_volume', 
    'alcohol_by_weight',
    'ibu',
    'description',
    ('batch', ('name')),
    ('preferred_vessel', ('name')),
    ('color', ('lovibond', 'ebc', 'hex', 'example')),
    ('variety', ('name', 'path', 'description')),
    'characteristics',
    ('brewery', ('id', 'name', 'url', 'rating', ('city',('id', 'city', 'state', 'province', 'country')))),
  )
  
  def url(self, object):
    return site_url + object.get_absolute_url()
  
  def characteristics(self, object):
    return [ tag.name for tag in Tag.objects.get_for_object(object) ]

class BeerHandler(BaseHandler):
  model = Beer
  anonymous = AnonymousBeerHandler

  
class AnonymousBeerRecommendedForHandler(AnonymousBeerHandler):
  def read(self, request, *args, **kwargs):
    user = get_object_or_404(User, username=kwargs['username'])
    return user.info.recommended_beers()

class BeerRecommendedForHandler(BeerHandler):
  anonymous = AnonymousBeerRecommendedForHandler


class AnonymousBeerFaveListHandler(AnonymousBeerHandler):
  def read(self, request, *args, **kwargs):
    fave_type = get_object_or_404(FaveType, slug=kwargs['fave_type_slug'])
    user = get_object_or_404(User, username=kwargs['username'])
    faves = Fave.objects.get_for_user(user, fave_type=fave_type)
    content_type = ContentType.objects.get_for_model(self.model)
    object_id_list = [ fave.content_object.pk for fave in faves if fave.content_type==content_type ]
    return self.model.objects.filter(pk__in=object_id_list)

class BeerFaveListHandler(BeerHandler):
  anonymous = AnonymousBeerFaveListHandler


class AnonymousBreweryHandler(AnonymousBaseHandler):
  model = Brewery
  fields = (
    'id', 
    'name', 
    'url', 
    'rating', 
    ('city',('id', 'city', 'state', 'province', 'country')),
  ),

  def url(self, object):
    return site_url + object.get_absolute_url()


class BreweryHandler(BaseHandler):
  model = Brewery
  anonymous = AnonymousBreweryHandler
