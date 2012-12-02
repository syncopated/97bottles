from django.db import models

class Tagline(models.Model):
  """
  A tagline is a short phrase for the site.
  """
  text = models.CharField(max_length=255)

  def __unicode__(self):
    return self.text
