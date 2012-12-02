"""
Template tags which can do retrieval of content from any model.

"""


from django import template
from django.db.models import get_model


class LatestObjectsNode(template.Node):
    def __init__(self, model, num, varname, manager=None):
        self.model, self.num, self.varname, self.manager = model, int(num), varname, manager
    
    def render(self, context):
        model = get_model(*self.model.split('.'))
        if model is not None:
            if self.num == 1:
                try:
                  if self.manager:
                      context[self.varname] = getattr(model, self.manager).all()[0]
                  else:
                      context[self.varname] = model._default_manager.all()[0]
                except: # Bad lookup: no matching object or too many matching objects.
                  pass
            else:
              try:
                if self.manager:
                    context[self.varname] = getattr(model, self.manager).all()[:self.num]
                else:
                    context[self.varname] = model._default_manager.all()[:self.num]
              except: # Bad lookup: no matching object or too many matching objects.
                pass
        return ''


class AllObjectsNode(template.Node):
    def __init__(self, model, varname):
        self.model, self.varname = model, varname

    def render(self, context):
        model = get_model(*self.model.split('.'))
        if model is not None:
            try:
              context[self.varname] = list(model._default_manager.all())
            except: # Bad lookup: no matching object or too many matching objects.
              pass
        return ''
                

class RandomObjectsNode(template.Node):
    def __init__(self, model, num, varname, manager=None):
        self.model, self.num, self.varname, self.manager = model, int(num), varname, manager
    
    def render(self, context):
        model = get_model(*self.model.split('.'))
        if model is not None:
            if self.num == 1:
                try:
                  if self.manager:
                      context[self.varname] = getattr(model, self.manager).order_by('?')[0]
                  else:
                      context[self.varname] = model._default_manager.order_by('?')[0]
                except: # Bad lookup: no matching object or too many matching objects.
                  pass
            else:
                try:
                  if self.manager:
                      context[self.varname] = getattr(model, self.manager).order_by('?')[:self.num]
                  else:
                      context[self.varname] = model._default_manager.order_by('?')[:self.num]
                except: # Bad lookup: no matching object or too many matching objects.
                  pass
        return ''


class GetObjectNode(template.Node):
    def __init__(self, model, pk, varname):
        self.model, self.pk, self.varname = model, pk, varname
    
    def render(self, context):
        model = get_model(*self.model.split('.'))
        if model is not None:
            try:
                context[self.varname] = model._default_manager.get(pk=self.pk)
            except (AssertionError, model.DoesNotExist): # Bad lookup: no matching object or too many matching objects.
                pass
        return ''


class GetObjectBySlugNode(template.Node):
    def __init__(self, model, slug, varname):
        self.model, self.slug, self.varname = model, slug, varname

    def render(self, context):
        model = get_model(*self.model.split('.'))
        if model is not None:
            try:
                context[self.varname] = model._default_manager.get(slug=self.slug)
            except (AssertionError, model.DoesNotExist): # Bad lookup: no matching object or too many matching objects.
                pass
        return ''

def do_latest_objects(parser, token):
    """
    Retrieves the latest ``num`` objects from a given model, in that
    model's default ordering, and stores them in a context variable.
    
    Syntax::
    
        {% get_latest_objects [app_name].[model_name] [num] as [varname] (with manager [manager_name]) %}
    
    Example::
    
        {% get_latest_objects comments.freecomment 5 as latest_comments with manager approved_comments %}
    
    """
    bits = token.contents.split()
    try:
      return LatestObjectsNode(bits[1], bits[2], bits[4], bits[7])
    except:
      return LatestObjectsNode(bits[1], bits[2], bits[4])

def do_get_all_objects(parser, token):
    """
    Retrieves the all objects from a given model, in that
    model's default ordering, and stores them in a context variable.

    Syntax::

        {% get_all_objects [app_name].[model_name] as [varname] %}

    Example::

        {% get_all_objects comments.freecomment as latest_comments %}

    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'%s' tag takes thre arguments" % bits[0])
    if bits [2] != 'as':
        raise template.TemplateSyntaxError("second argument to '%s' tag must be 'as'" % bits[0])
    return AllObjectsNode(bits[1], bits[3])


def do_random_objects(parser, token):
    """
    Retrieves ``num`` random objects from a given model, and stores
    them in a context variable.
    
    Syntax::
    
        {% get_random_objects [app_name].[model_name] [num] as [varname] (with manager [manager_name]) %}
    
    Example::
    
        {% get_random_objects comments.freecomment 5 as random_comments %}
    
    """
    bits = token.contents.split()
    try:
      return RandomObjectsNode(bits[1], bits[2], bits[4], bits[7])
    except:
      return RandomObjectsNode(bits[1], bits[2], bits[4])

def do_get_object(parser, token):
    """
    Retrieves a specific object from a given model by primary-key
    lookup, and stores it in a context variable.
    
    Syntax::
    
        {% retrieve_object [app_name].[model_name] [pk] as [varname] %}
    
    Example::
    
        {% retrieve_object flatpages.flatpage 12 as my_flat_page %}
    
    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise template.TemplateSyntaxError("'%s' tag takes four arguments" % bits[0])
    if bits[3] != 'as':
        raise template.TemplateSyntaxError("third argument to '%s' tag must be 'as'" % bits[0])
    return GetObjectNode(bits[1], bits[2], bits[4])


def do_get_object_by_slug(parser, token):
    """
    Retrieves a specific object from a given model by primary-key
    lookup, and stores it in a context variable.

    Syntax::

        {% get_object_by_slug [app_name].[model_name] [slug] as [varname] %}

    Example::

        {% get_object_by_slug media.Photo jeff-croft-headshot as headshot %}

    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise template.TemplateSyntaxError("'%s' tag takes four arguments" % bits[0])
    if bits[3] != 'as':
        raise template.TemplateSyntaxError("third argument to '%s' tag must be 'as'" % bits[0])
    return GetObjectBySlugNode(bits[1], bits[2], bits[4])

register = template.Library()
register.tag('get_latest_objects', do_latest_objects)
register.tag('get_random_objects', do_random_objects)
register.tag('get_object', do_get_object)
register.tag('get_object_by_slug', do_get_object_by_slug)
register.tag('get_all_objects', do_get_all_objects)

