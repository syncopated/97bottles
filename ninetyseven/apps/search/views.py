from haystack.views import *

from ninetyseven.apps.search.forms import *

def search(request, template="search/search.html"):
  """
  This is just a wrapper around Haystack's regular search view.
  """
  return SearchView(form_class=SearchForm, template=template).__call__(request)
