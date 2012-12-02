from savoy.utils.path import append_third_party_path
append_third_party_path()

import logging
import urllib

from django.conf import settings
from django.utils.encoding import smart_unicode
from django.template.defaultfilters import slugify

from savoy.contrib.bookmarks.models import Bookmark, MagnoliaBookmark
from savoy.utils import importers

#
# Magnolia client, based on one by Rob Hudson
#
class MagnoliaClient(object):
    """
    A super-minimal Magnolia client :)
    """
    def __init__(self, api_key, method=None):
        self.api_key = api_key
        self.method = method
        
    def __getattr__(self, method):
        return MagnoliaClient(self.api_key, method)
        
    def __repr__(self):
        return "<MagnoliaClient: %s>" % self.method
        
    def __call__(self, **params):
        params['api_key'] = self.api_key
        url = ("http://ma.gnolia.com/api/rest/1/%s/?" % (self.method)) + urllib.urlencode(params)
        return importers.getxml(url)

#
# Public API
#

def enabled():
    return hasattr(settings, 'MAGNOLIA_API_KEY') and hasattr(settings, 'MAGNOLIA_USERNAME')
    
def update():
    magnolia = MagnoliaClient(settings.MAGNOLIA_API_KEY)
    params = {'person': settings.MAGNOLIA_USERNAME}
    xml = magnolia.bookmarks_find(**params)
    _update_bookmarks(xml)
                
#
# Private API
#

def _update_bookmarks(xml):
    for bookmark in xml.getiterator('bookmark'):
        info = dict((k, smart_unicode(bookmark.get(k))) for k in bookmark.keys())
        for e in bookmark.getchildren():
          if e.tag == 'tags':
            info['tags'] = ', '.join([t.get('name') for t in e.getchildren()])
          else:
            info[e.tag] = e.text
        _handle_bookmark(info)
        
def _handle_bookmark(info):
    if info['private'] == 'false':
        try:
          mag_bookmark = MagnoliaBookmark.objects.get(magnolia_id=info['id'])
          bookmark = mag_bookmark.bookmark
        except:
          mag_bookmark = MagnoliaBookmark(magnolia_id=info['id'])
          bookmark = Bookmark (
            url = info['url'],
          )

        bookmark.title          = info['title']
        bookmark.description    = info.get('description', '')
        bookmark.screenshot     = info.get('screenshot', '')
        bookmark.date_published = importers.parsedate(info['created'])
        bookmark.date_updated   = importers.parsedate(info['updated'])
        bookmark.rating         = info.get('rating', None)
        bookmark.private        = False
        bookmark.slug           = slugify(info['title'])
        bookmark.tags           = info.get('tags', '')
        bookmark.save()
        try:
          mag_bookmark.bookmark = bookmark
          mag_bookmark.save()
        except:
          bookmark.delete()
          
          
if __name__ == '__main__':
    update()