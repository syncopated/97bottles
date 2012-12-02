import datetime

from django.db import models
from tagging.fields import TagField

class Quotation(models.Model):
    quote               = models.TextField()
    author              = models.CharField(blank=True, max_length=200)
    author_affiliation  = models.CharField(blank=True, max_length=100)
    url                 = models.URLField(blank=True, null=True, max_length=200)
    slug                = models.SlugField(unique_for_date="date_published")
    date_published      = models.DateTimeField(help_text="Select the date and time this entry was posted.", default=datetime.datetime.now)
    date_created        = models.DateTimeField(editable=False, default=datetime.datetime.now)
    tags                = TagField(help_text="Add tags for this quote (space separated).")

    def __unicode__(self):
      return self.author + ': ' + self.quote