from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType

from faves.models import Fave
from tagging.fields import TagField
from tagging.models import Tag
from savoy.core.geo.models import City, GeolocatedItem

from ninetyseven.apps import BaseModel
from ninetyseven.apps.beers.models import Beer, Vessel, ServingType

class Review(BaseModel):
  """
  A review of a Beer, by a user.
  """
  beer            = models.ForeignKey(Beer, related_name="reviews")
  rating          = models.PositiveIntegerField(help_text="Rate this beer on a scale of 1-97 (97 being completely, unbelievably delicious)")
  comment         = models.TextField(blank=True, help_text="Tell us what you think about this beer!")
  characteristics = TagField(blank=True, null=True, help_text="Use tags such as `nutty','bitter', and `brown' to describe this beer. Separate tags with spaces or commas.")
  vessel          = models.ForeignKey(Vessel, help_text="The kind of container you drank this beer from.")
  serving_type    = models.ForeignKey(ServingType, blank=True, null=True, help_text="From a tap? Keg? Tell us how this beer was served.")
  city            = models.ForeignKey(City, blank=True, null=True, related_name="reviews", help_text="Where were you when you drank this beer? If you can not find your city, add it!")
  
  ip_address      = models.IPAddressField(blank=True, null=True)
  is_public       = models.BooleanField(default=True, help_text='Uncheck this box to make the review effectively disappear from the site.')
  is_removed      = models.BooleanField(default=False, help_text='Check this box if the review is inappropriate. A "This comment has been removed" message will be displayed instead.')
  
  class Meta:
    ordering = ('-date_created',)
    get_latest_by = 'date_created'
  
  def __unicode__(self):
    return u"%s, on %s" % (self.created_by, self.beer)

  def get_absolute_url(self):
    """
    Returns the URL to this review.
    """
    beer_url = self.beer.get_absolute_url()
    return "%s#review-%s" % (beer_url, str(self.id))
  
  def _serialize(self):
    obj = {
      "id": self.pk,
      "beer_id": self.beer.id,
      "rating": self.rating,
      "comment": self.comment,
      "url": 'http://97bottles.com%s' % self.get_absolute_url(),
      "vessel": getattr(getattr(self, 'vessel', None), 'name', None),
      "serving_type": getattr(getattr(self, 'serving_type', None), 'name', None),
      "characteristics": [ tag.name for tag in Tag.objects.get_for_object(self) ],
      "city": {
        "id": getattr(getattr(self, 'city', None), 'id', None),
        "name": getattr(getattr(self, 'city', None), 'city', None),
        "state": getattr(getattr(self, 'city', None), 'state', None),
        "province": getattr(getattr(self, 'city', None), 'province', None),
        "country": getattr(getattr(self, 'city', None), 'country', None),
      },
    }
    return obj
  
  def save(self, force_insert=False, force_update=False):
    """ Saves the review, and then creates or updates the GeolocatedItem object associated with it. """
    try:
      # If the user has this beer in his/he to-drink list, remove it.
      beer_content_type = ContentType.objects.get_for_model(Beer)
      fave = Fave.objects.get(type__slug="to-dos", user=self.created_by, content_type=beer_content_type, object_id=self.beer.id)
      fave.withdrawn = True
      fave.save()
    except Fave.DoesNotExist:
      pass
    super(Review, self).save(force_insert=force_insert, force_update=force_update)
    if self.city:
      GeolocatedItem.objects.create_or_update(self, address=self.city.full_name_ascii(), city=self.city)