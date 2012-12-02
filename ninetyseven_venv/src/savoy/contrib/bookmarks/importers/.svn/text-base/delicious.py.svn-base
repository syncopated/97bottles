from savoy.utils.path import append_third_party_path
append_third_party_path()

import time
import datetime
import logging
import urllib

from django.conf import settings
from django.db import transaction
from django.utils.encoding import smart_unicode
from django.template.defaultfilters import slugify

from savoy.contrib.bookmarks.models import Bookmark, DeliciousBookmark
from savoy.utils import importers

#
# Super-mini Delicious API
# Nabbed (and modified) from Jacob's Jellyroll.
#
class DeliciousClient(object):
    """
    A super-minimal delicious client :)
    """
    
    lastcall = 0
    
    def __init__(self, username, password, method='v1'):
        self.username, self.password = username, password
        self.method = method
        
    def __getattr__(self, method):
        return DeliciousClient(self.username, self.password, '%s/%s' % (self.method, method))
        
    def __repr__(self):
        return "<DeliciousClient: %s>" % self.method
        
    def __call__(self, **params):
        # Enforce Yahoo's "no calls quicker than every 1 second" rule
        delta = time.time() - DeliciousClient.lastcall
        if delta < 2:
            time.sleep(2 - delta)
        DeliciousClient.lastcall = time.time()
        url = ("https://api.del.icio.us/%s?" % self.method) + urllib.urlencode(params)
        return importers.getxml(url, username=self.username, password=self.password)

#
# Public API
#

def enabled():
    return hasattr(settings, 'DELICIOUS_USERNAME') and hasattr(settings, 'DELICIOUS_PASSWORD')
    
def update():
    delicious = DeliciousClient(settings.DELICIOUS_USERNAME, settings.DELICIOUS_PASSWORD)
    _update_bookmarks(delicious)
                
#
# Private API
#

@transaction.commit_on_success
def _update_bookmarks(delicious):
    xml = delicious.posts.all()
    for post in xml.getiterator('post'):
      info = dict((k, smart_unicode(post.get(k))) for k in post.keys())
      _handle_bookmark(info)

def _handle_bookmark(info):
    try:
      del_bookmark = DeliciousBookmark.objects.get(hash=info['hash'])
      bookmark = del_bookmark.bookmark
    except:
      del_bookmark = DeliciousBookmark(hash=info['hash'])
      bookmark = Bookmark (
        url = info['href'],
      )

    offset                  = 8+settings.UTC_OFFSET
    time_difference         = datetime.timedelta(hours=offset)
    
    bookmark.title          = info['description']
    bookmark.description    = info.get('extended', '')
    bookmark.date_published = importers.parsedate(info['time']) + time_difference
    bookmark.slug           = slugify(info['description'])
    bookmark.tags           = info.get('tag', '')
    bookmark.save()

    del_bookmark.bookmark = bookmark
    del_bookmark.save()



if __name__ == '__main__':
    update()