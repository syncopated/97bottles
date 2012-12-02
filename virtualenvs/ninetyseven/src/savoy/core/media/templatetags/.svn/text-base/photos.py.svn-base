from __future__ import division

from django import template
from django.template import Library
from django.conf import settings

from savoy.core.media.models import *

register = Library()


class GetPhotosWithTagNode(template.Node):
    def __init__(self, type, num, varname):
      self.tag, self.num, self.varname = type, num, varname

    def render(self, context):
      from tagging.models import Tag, TaggedItem
      try:
        tag = Tag.objects.get(name=self.tag)
        context[self.varname] = TaggedItem.objects.get_by_model(Photo, tag).order_by('-date_published')[:self.num]
      except:
        pass
      return ''

@register.tag
def get_photos_with_tag(parser, token):
    """
    Retrieves a given number of photos that have related FlickrPhoto objects sorted by date_published.

    Syntax::

        {% get_photos_with_tag [tag] [num] as [varname] %}

    Example::

        {% get_photos_with_tag screenshot 5 as screenshot_list %}

    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise template.TemplateSyntaxError("'%s' tag takes four arguments" % bits[0])
    #if bits[1] != 'attend' or 'watch' or 'all':
    #    raise template.TemplateSyntaxError("first argument to '%s' tag must be 'attend', 'watch', or 'all'." % bits[0])
    if bits[3] != 'as':
        raise template.TemplateSyntaxError("third argument to '%s' tag must be 'as'" % bits[0])
    return GetPhotosWithTagNode(bits[1], bits[2], bits[4])


class GetLatestFlickrPhotosNode(template.Node):
    def __init__(self, type, num, varname):
      self.type, self.num, self.varname = type, num, varname

    def render(self, context):
      if self.type == 'personal':
        context[self.varname] = Photo.objects.filter(flickrphoto__isnull=False, flickrphoto__owner__nsid=settings.FLICKR_USERID).order_by('-date_published')[:self.num]
      elif self.type == 'favorites':
        context[self.varname] = Photo.objects.filter(flickrphoto__isnull=False).exclude(flickrphoto__owner__nsid=settings.FLICKR_USERID).order_by('-date_published')[:self.num]
      else:
        context[self.varname] = Photo.objects.filter(flickrphoto__isnull=False).order_by('-date_published')[:self.num]
      return ''

@register.tag
def get_latest_flickr_photos(parser, token):
    """
    Retrieves a given number of photos that have related FlickrPhoto objects sorted by date_published.

    Syntax::

        {% get_latest_flickr_photos [type(favorites|personal|all)] [num] as [varname] %}

    Example::

        {% get_latest_flickr_photos personal 5 as latest_photos %}

    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise template.TemplateSyntaxError("'%s' tag takes four arguments" % bits[0])
    #if bits[1] != 'attend' or 'watch' or 'all':
    #    raise template.TemplateSyntaxError("first argument to '%s' tag must be 'attend', 'watch', or 'all'." % bits[0])
    if bits[3] != 'as':
        raise template.TemplateSyntaxError("third argument to '%s' tag must be 'as'" % bits[0])
    return GetLatestFlickrPhotosNode(bits[1], bits[2], bits[4])


@register.filter
def convert_for_width(value, new_size):
  percentage = new_size/500
  return value * percentage
  
  
@register.simple_tag
def convert_note_size(note, value, new_width):
  """
  When displaying photos at a different size than Flickr does on its photo pages,
  you must convert notes to the size you're displaying at. Given a note, a value (of w, h, x, or y),
  and the width of your scaled version, this template tag will return the converted value.
  
  Example usage:
  <div style="position: absolute; height: {% convert_note_size note 'h' 470 %}px; width: {% convert_note_size note 'w' 470 %}px; top: {% convert_note_size note 'y' 470 %}px; left: {% convert_note_size note 'x' 470 %}px">
  """
  photo = note.flickr_photo.photo
  try:
    scale_percentage = new_width / photo.image_width
  except:
    return ''

  if photo.is_horizontal():
    percentage = new_width / 500 
  elif photo.is_vertical():
    aspect_ratio = photo.image_height / photo.image_width
    new_height = new_width * aspect_ratio
    percentage = new_height / 500

  if value == 'h':
    return note.h * percentage
  if value == 'w':
    return note.w * percentage
  if value == 'y':
    return note.y * percentage
  if value == 'x':
    return note.x * percentage