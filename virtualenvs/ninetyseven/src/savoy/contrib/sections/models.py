import datetime

from django.db import models
from tagging.models import Tag

from savoy.core.tags.utils.tags import get_items_for_tags

class Section(models.Model):
    """
    A section aggregates tags in a page or pages on the site.
    """
    
    title               = models.CharField(max_length=100, help_text='Enter the name of this section.')
    slug                = models.SlugField(help_text='The slug is a URL-friendly version of the title. It is auto-populated.')
    description         = models.TextField(blank=True, help_text='Enter a description for this section.')
    tags                = models.ManyToManyField(Tag)
    
    date_created        = models.DateTimeField(default=datetime.datetime.now, editable=False)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
      return "/sections/%s/" % (self.slug)
    
    def tag_list(self):
      """ Returns a list of tag names for this section. """
      tag_list = []
      for tag in self.tags.all():
        tag_list.append(tag.name)
      return tag_list
    
    def items(self):
      return get_items_for_tags(self.tag_list(), method="any")