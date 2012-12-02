from django import template
from savoy.contrib.bookmarks.models import Bookmark

register = template.Library()

@register.simple_tag
def description_with_link(bookmark, link_string=None):
  if not link_string:
    link_string = "Visit &raquo;"
  link = ' <a href="%s" title="%s">%s</a>' % (bookmark.url, bookmark.title, link_string)
  return bookmark.description + link
  
  