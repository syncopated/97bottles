import datetime

from django.db import models
from django.contrib.markup.templatetags.markup import *

from savoy.core.media.models import Photo
from savoy.core.constants import STATUS_CHOICES, MARKUP_CHOICES
from savoy.core.pages.managers import *

class PageTemplate(models.Model):
  name                = models.CharField(max_length=255, help_text="Enter the name of this template, i.e. 'Three Column'.")
  path                = models.CharField(max_length=255, help_text="Enter the path to this template. Do not include a leading slash, i.e. 'pages/templates/three_column.html'.")

  def __unicode__(self):
    return self.name


class Page(models.Model):
    url               = models.CharField(max_length=100, help_text="Example: '/about/contact/'. Make sure to have leading and trailing slashes.")
    title             = models.CharField(max_length=200, help_text="Enter the title of this page.")
    subhead           = models.CharField(max_length=200, blank=True, help_text="Enter the subheader for this page.")
    photo             = models.ForeignKey(Photo, blank=True, null=True, help_text="Select or add a photo for use on this page.")
    primary_content   = models.TextField(blank=True, help_text="Enter the content of the primary page area. Valid (X)HTML is accept, but a simpler markup language (Markdown, Textile, etc.) is preferred.")
    secondary_content = models.TextField(blank=True, help_text="Enter the content of the secondary page area. Valid (X)HTML is accept, but a simpler markup language (Markdown, Textile, etc.) is preferred.")
    fine_print        = models.TextField(blank=True, help_text="Enter the content of the fine print page area. Valid (X)HTML is accept, but a simpler markup language (Markdown, Textile, etc.) is preferred.")
    pub_date          = models.DateTimeField('Date published', help_text="Select the date and time this page should be posted.", default=datetime.datetime.now)
    status            = models.IntegerField(help_text="Select the status of this page.", choices=STATUS_CHOICES, default=2)
    markup_language   = models.CharField(max_length=100, default="markdown", choices=MARKUP_CHOICES, help_text="Select the markup language you would like to process this content with.")
    template          = models.ForeignKey(PageTemplate, blank=True, null=True, help_text="Select a template for this page. If no template is selected, a template will be looked for at the associated path for this URL (i.e. a URL of '/about/contact' will look in 'pages/about/contact.html'). If a template is still not found, 'pages/default.html' will be used.")
    objects           = models.Manager()
    live_pages        = LivePageManager()

    def __str__(self):
        return "%s - %s" % (self.url, self.title)
    
    def get_absolute_url(self):
      """ Returns the URL to this page. """
      return self.url
        
    def _render_markup(self, value):
      import markdown
      if self.markup_language == None:
        return value
      elif self.markup_language == 'markdown':
        return markdown.markdown(value, safe_mode=False)
      elif self.markup_language == 'textile':
        return textile(value)
      elif self.markup_language == 'restructuredtext':
        return restructuredtext(value)
      else:
        return value
    
    def primary_content_rendered_markup(self):
      """ The primary content field, with any markup filters applied. """
      return self._render_markup(self.primary_content)
    
    def secondary_content_rendered_markup(self):
      """ The secondary content field, with any markup filters applied. """
      return self._render_markup(self.secondary_content)
    
    def fine_print_rendered_markup(self):
      """ The fine print field, with any markup filters applied. """
      return self._render_markup(self.fine_print)