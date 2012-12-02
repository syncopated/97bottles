from django import template
from tagging.models import Tag, TaggedItem
from django.contrib.contenttypes.models import ContentType

register = template.Library()

class TagsByPopularityNode(template.Node):
    def __init__(self, num, varname, model=None):
        self.num, self.varname, self.model = int(num), varname, model

    def render(self, context):
      from django.template.defaultfilters import dictsortreversed
      try:
        tags = []
        
        if self.model:
          app_label, model_name = self.model.split('.')
          content_types = [ContentType.objects.get(app_label=app_label, model=model_name)]
        else:
          content_types = ContentType.objects.all()

        item_count = 0
        for content_type in content_types:
          model = content_type.model_class()
          if hasattr(model, 'tags'):
            item_count = item_count + model.objects.all().count()
            ct_tags = Tag.objects.usage_for_model(model, counts=True)
            for tag in ct_tags:
              tags.append(tag)
      
        context[self.varname] = dictsortreversed(tags, 'count')[:self.num]
        context['tagged_item_count'] = item_count
      except:
        pass
      return ''



@register.tag
def get_tags_by_popularity(parser, token):
    """
    Retrieves the latest ``num`` Tag object, based on their usage across all models, and stores them in the specified context variable.
    Also adds a ``tagged_item_count`` variable to the context, which is the total number of content objects in the system that have been tagged.
    Optionally, takes a model name, and only gets results for that model.

    Syntax::

        {% get_tags_by_popularity [num] as [varname] (for [appname.model]) %}

    Example::

        {% get_tags_by_popularity 10 as tag_list for blogs.entry %}

    """
    bits = token.contents.split()
    try:
      return TagsByPopularityNode(bits[1], bits[3], model=bits[5])
    except:
      return TagsByPopularityNode(bits[1], bits[3])