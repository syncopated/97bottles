from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_detail, object_list

from tagging.models import *

from ninetyseven.apps.beers.models import Beer

def tag_list(request, template_name="tags/tag_list.html", template_object_name="tag", extra_context={}):
  extra = {}
  extra.update(extra_context)
  return object_list(
    request,
    queryset=Tag.objects.all(),  
    template_object_name=template_object_name,
    template_name=template_name,
    extra_context=extra,
  )

def tag_detail(request, tag, template_name="tags/tag_detail.html", template_object_name="tag", extra_context={}):
  tag = get_object_or_404(Tag, name=tag)
  extra = {
    'beer_list': TaggedItem.objects.get_by_model(Beer, tag),
  }
  extra.update(extra_context)
  return object_detail(
    request,
    template_name = template_name,
    template_object_name = template_object_name,
    object_id = tag.id,
    queryset = Tag.objects.all(),
    extra_context = extra,
  )