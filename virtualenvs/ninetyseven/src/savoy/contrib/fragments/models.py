from django.db import models

from savoy.core.constants import MARKUP_CHOICES

class Fragment(models.Model):
  """
  A Fragment is a piece of content associated with a unique key that can
  be inserted into any template with the use of the fragment template tag.
  """
  key               = models.CharField(help_text="A unique name for this fragment of content", blank=False, max_length=255, unique=True)
  content           = models.TextField(blank=True)
  markup_language   = models.CharField(max_length=100, default=None, choices=MARKUP_CHOICES, help_text="Select the markup language you would like to process this content with.")
  
  def __unicode__(self):
      return u"%s" % (self.key,)
