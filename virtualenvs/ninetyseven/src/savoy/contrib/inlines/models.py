from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify

class InlineType(models.Model):
  """
  An InlineType is an object that can be inserted into a blog entry or other text.
  """
  name          = models.CharField(max_length=200, help_text="Enter the display name for this inline type, such as 'Photo' or 'Video'.")
  content_type  = models.ForeignKey(ContentType, help_text="Select the content type for this inline type.")
  slug          = models.SlugField(unique=True)
  template      = models.CharField(editable=False, max_length=250)
  
  def save(self, force_insert=False, force_update=False):
    """ Creates the template path, then saves the InlineType object. """
    self.template = "inlines/%s%s" % (self.slug, ".html")
    super(InlineType, self).save(force_insert=force_insert, force_update=force_update) # Call the "real" save() method

  def __unicode__(self):
    return self.name
