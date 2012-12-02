
import datetime

import httplib2
import dateutil.parser
import dateutil.tz
from django.utils import simplejson
from django.utils.encoding import force_unicode
from django.conf import settings

from savoy.utils.anyetree import etree

#
# Straight up stolen from Jacob's Jellyroll (http://code.google.com/p/jellyroll/)
# and slighty modified.
#

DEFAULT_HTTP_HEADERS = {
    "User-Agent" : "Savoy/1.0"
}

#
# URL fetching sugar
#
    
def getxml(url, **kwargs):
    """Fetch and parse some XML. Returns an ElementTree"""
    xml = fetch_resource(url, **kwargs)
    try:
      return etree.fromstring(xml)
    except SyntaxError:
      print "\n\nERROR: API did not return a valid XML file.\n\n"
      raise
    
def getjson(url, **kwargs):
    """Fetch and parse some JSON. Returns the deserialized JSON."""
    json = fetch_resource(url, **kwargs)
    return simplejson.loads(json)

def fetch_resource(url, method="GET", body=None, username=None, password=None, headers=None):
    h = httplib2.Http(timeout=15)
    h.force_exception_to_status_code = True
    if username is not None or password is not None:
        h.add_credentials(username, password)
    
    if headers is None:
        headers = DEFAULT_HTTP_HEADERS.copy()
    
    response, content = h.request(url, method, body, headers)
    return content
    
#
# Date handling utils
#

def parsedate(s):
    """
    Convert a string into a (local, naive) datetime object.
    """
    dt = dateutil.parser.parse(s)
    if dt.tzinfo:
        dt = dt.astimezone(dateutil.tz.tzlocal()).replace(tzinfo=None)
    return dt
            
def safeint(s):
    """Always returns an int. Returns 0 on failure."""
    try:
        return int(force_unicode(s))
    except (ValueError, TypeError):
        return 0