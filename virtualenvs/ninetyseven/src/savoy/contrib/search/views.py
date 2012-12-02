from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

def perform_search(request, page=None, paginate_by=30, allow_empty=True):
  
  # Create a list of models to be searched
  # By default, this is all models in the settings.SEARCH_MODELS list
  search_models = []
  for item in settings.SEARCH_MODELS:
    search_models.append(item['model'])
  
  # If the search form parameters included a "models" key, then re-create the list
  # of models to be searched based on the value of that key.
  # A value of "everything" will skip this step, resulting in a search of all models in
  # settings.SEARCH_MODELS.
  if request.GET.__contains__('models'):
    model_string = request.GET['models']
    if not request.GET['models'] == "everything":
      search_models   = request.GET['models'].split(",")
  else:
    model_string = "everything"

  if request.GET.__contains__('search'):
    search_string     = request.GET['search']
    
    # First, split on double-quotes to extract any multi-word terms
    search_terms      = search_string.split('"')
    cleaned_search_terms = []
    
    # Then, remove any unnecessary whitespace at the beginings or ends of the terms
    for item in search_terms:
      if not item.startswith(' ') and not item.endswith(' ') and not item == '':
        cleaned_search_terms.append(item)
      if item.startswith(' '):
        cleaned_search_terms.append(item[1:])
      if item.endswith(' '):
        cleaned_search_terms.append(item[:-1])
  
    # Set up a list to put results into
    search_results    = []
    results           = None
  
    # Search each model for the search term, as long as that model is in both settings.SEARCH_MODELS
    # and our search_models list.
    for item in settings.SEARCH_MODELS:
      if unicode(item['model']) in search_models:
        app_label     = item['model'].split('.')[0]
        model         = item['model'].split('.')[1]
        content_type  = ContentType.objects.get(app_label=app_label, model=model)
        model         = content_type.model_class()
        try:
          manager     = getattr(model, item['manager'])
        except:
          manager     = model._default_manager
        opts          = model._meta
        query         = Q()
        queries       = []

        for term in cleaned_search_terms:
          for field in item['fields']:
            lookup    = field + "__icontains"
            kwargs    = { lookup: term }
            q         = Q(**kwargs)
            queries.append(q)
    
        for q in queries:
          query       = query | q
    
          results     = manager.filter(query)

        # For each result, return a dict containing the model, the object, and some metadata about the model.
        if results:
          for result in results:
            result_dict   = { 'model': item['model'], 'object': result, 'model_class': model._meta.verbose_name, 'model_verbose_name_plural': model._meta.verbose_name_plural }
            search_results.append(result_dict)

    context = RequestContext(request, { 
      'search_terms': search_terms,
      'search_string': search_string,
      'model_string' : model_string,
      'results': search_results,
      'hits': len(search_results),
    })
    return render_to_response('search/results.html', context)
  else:
    context = RequestContext(request, 
      {}
    )
    return render_to_response('search/form.html', context)