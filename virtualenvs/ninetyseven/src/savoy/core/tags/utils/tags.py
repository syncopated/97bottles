import datetime

from django.http import Http404, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from tagging.models import Tag, TaggedItem

from savoy.core.geo.models import GeolocatedItem
from savoy.utils.date_sort import sort_items_by_date

def tag_list(request):
  from django.views.generic.list_detail import object_list
  from django.template.defaultfilters import dictsortreversed
  tags = Tag.objects.all()
  tags_by_popularity = []

  content_types = ContentType.objects.all()
  item_count = 0
  for content_type in content_types:
    model = content_type.model_class()
    if hasattr(model, 'tags'):
      item_count = item_count + model.objects.all().count()
      ct_tags = Tag.objects.usage_for_model(model, counts=True)
      for tag in ct_tags:
        tags_by_popularity.append(tag)

  tags_by_popularity = dictsortreversed(tags_by_popularity, 'count')

  extra_context = {
    'tagged_item_count': item_count,
    'tags_by_popularity': tags_by_popularity,
    'most_popular_tag': tags_by_popularity[0],
  }
  return object_list(
    request,
    queryset=tags,  
    template_object_name='tag',
    template_name='sections/tag_list.html',
    extra_context=extra_context,
  )


def tag_detail(request, tag, paginate_by=30, page=None, allow_empty=True):
  from django.views.generic.list_detail import object_detail
  
  try:
    # If there's a section with this tag name, redirect to it's URL.
    from savoy.contrib.sections.models import Section
    section = Section.objects.get(slug=tag)
    return HttpResponseRedirect(section.get_absolute_url())
  except:
    pass
    
  try:
    # Look for a tag with this name.
    tags = Tag.objects.filter(name=tag)
    tag = Tag.objects.get(name=tag)
  except:
    raise Http404
  
  tagged_items = sort_items_by_date(get_items_for_tags(tag), recent_first=True)
  
  extra_context = { 
    'tagged_items': tagged_items,
  }
  
  # Return a tag detail page.
  return object_detail(
    request, 
    queryset=tags,
    object_id=tag.id,
    template_object_name='tag',
    template_name='sections/tag_detail.html',
    extra_context=extra_context,
  )


def get_items_for_tags(tag_list, method="any", models=None):
  """
  Given a list of tags, retrieves associated items. If the method argument is "any", the result is 
  items that match any of the tags in the list. If it's "all", the result is items that match all
  tags in the list. Optionally accepts a list of models to search. If models is not provided, searches
  all models with a TagField.
  """
  from tagging.generic import fetch_content_objects
  if not models:
    models = []
    for content_type in ContentType.objects.all():
      model = content_type.model_class()
      if hasattr(model, 'tags'):
        models.append(model)
  tagged_items = []
  for model in models:
    if method == "all":
      model_tagged_items = TaggedItem.objects.get_intersection_by_model(model, tag_list)
    else:
      model_tagged_items = TaggedItem.objects.get_union_by_model(model, tag_list)
    tagged_items.extend(model_tagged_items)
  return tagged_items