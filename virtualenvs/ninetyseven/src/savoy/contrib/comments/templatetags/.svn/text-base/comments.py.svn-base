from django import forms
from django import template
from django.template import resolve_variable
from django.contrib.contenttypes.models import ContentType

from savoy.contrib.comments.models import *
from savoy.contrib.comments.forms import *

register = template.Library()

@register.inclusion_tag('comments/comment_form.html', takes_context=True)
def display_comment_form(context, object):
  """
  Renders the comment form for a given object.
  
  {% display_comment_form entry %}
  """
  if context.has_key('preview'):
    preview = True
  else:
    preview = False
    
  return {
    'user': context['user'],
    'object_commenting_on': object,
    'preview': preview,
    'comment_form': CommentForm(instance=Comment()),
    'comment_target_content_type': ContentType.objects.get_for_model(object).id,
    'comment_target_object_id': object._get_pk_val(),
  }


@register.inclusion_tag('comments/comment_list.html', takes_context=True)
def display_comment_list(context, object):
  """
  Renders the list of comments for a given object.

  {% display_comment_list entry %}
  """
  content_type = ContentType.objects.get_for_model(object)
  comments = Comment.approved_comments.filter(content_type=content_type.id, object_id=object.id).order_by('date_submitted')
  return {
    'user': context['user'],
    'comment_list': comments 
  }


class CommentListNode(template.Node):
  def __init__(self, object, varname):
    self.object = object
    self.varname = varname

  def render(self, context):
    try:
      object = resolve_variable(self.object, context)
      content_type = ContentType.objects.get_for_model(object)
      comments = Comment.approved_comments.filter(content_type=content_type.id, object_id=object.id).order_by('date_submitted')
      context[self.varname] = comments
    except:
      pass
    return ''

@register.tag
def get_comment_list(parser, token):
    """
    Adds the list of comments for the given object to the current context.
    
    {% get_comment_list for entry as comment_list %}
    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise template.TemplateSyntaxError, "'%s' tag takes four arguments" % bits[0]
    if bits[1] != "for":
        raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'for'" % bits[0]
    if bits[3] != "as":
        raise template.TemplateSyntaxError, "Third argument to '%s' tag must be 'as'" % bits[0]
    
    return CommentListNode(bits[2], bits[4])


def get_comments_for_object(object):
  content_type = ContentType.objects.get_for_model(object)
  all_comments = []
  comments = Comment.approved_comments.filter(content_type=content_type.id, object_id=object.id).order_by('date_submitted')
  for comment in comments:
    all_comments.append(comment)
    child_comments = get_comments_for_object(comment)
    for child_comment in child_comments:
      all_comments.append(comment)
  return all_comments

class CollapsedCommentListNode(template.Node):
  def __init__(self, object, varname):
    self.object = object
    self.varname = varname

  def render(self, context):
    object = resolve_variable(self.object, context)
    comments = get_comments_for_object(object)
    context[self.varname] = comments
    return ''

@register.tag
def get_collapsed_comment_list(parser, token):
    """
    Adds the list of comments for the given object to the current context,
    collapsing any threads along the way.

    {% get_collapsed_comment_list for entry as comment_list %}
    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise template.TemplateSyntaxError, "'%s' tag takes four arguments" % bits[0]
    if bits[1] != "for":
        raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'for'" % bits[0]
    if bits[3] != "as":
        raise template.TemplateSyntaxError, "Third argument to '%s' tag must be 'as'" % bits[0]

    return CollapsedCommentListNode(bits[2], bits[4])
  