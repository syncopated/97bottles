import urllib2
from urllib import urlencode


def import_one_of(*args):
    for mod in args:
        try:
            return __import__(mod, "", "", [""])
        except ImportError:
            continue
    raise ImportError("Couldn't import any on %r" % args)

from savoy.utils.anyetree import etree

ET = etree

USER_AGENT = "Savoy 1.0"

def fetch_and_parse_xml(url, auth_info=None):
    """
    Fetch an XML document (possibly given auth info) and return an ElementTree.
    """
    return ET.parse(fetch_resource(url, auth_info))

def fetch_resource(url, auth_info):
    """
    Fetch a resource and return the file-like object.
    """
    if auth_info:
        handler = urllib2.HTTPBasicAuthHandler()
        handler.add_password(*auth_info)
        opener = urllib2.build_opener(handler)
    else:
        opener = urllib2.build_opener()

    request = urllib2.Request(url)
    request.add_header("User-Agent", USER_AGENT)
    return opener.open(request)

class UrbanMappingClient(object):
    def __init__(self, method=''):
        self.method = method

    def __getattr__(self, method):
        return UrbanMappingClient('%s.%s' % (self.method, method))

    def __repr__(self):
        return "<UrbanMappingClient: %s>" % self.method

    def __call__(self, **params):
        url = "http://api0.urbanmapping.com/neighborhoods/rest/" + self.method + "?" + urlencode(params) + "&format=xml"
        response = fetch_and_parse_xml(url)
        return response