
from django import template
from django.template import Library, Node
from django.template import resolve_variable

register = Library()

from ninetyseven.apps.invites.models import *

class GetInvitesNode(template.Node):
  def __init__(self, user, varname):
    self.user = user
    self.varname = varname

  def render(self, context):
    user = resolve_variable(self.user, context)
    context[self.varname] = Invite.objects.filter(user=user, email="", activation_key="")
    return ''

@register.tag
def get_invites (parser, token):
  """
  Returns all breweries, ordered by rating (highest first).

  Syntax::

      {% get_invites for [user] as [varname] %}

  Example::

      {% get_invites for user as invite_list %}

  """
  bits = token.contents.split()
  if len(bits) == 5:
    return GetInvitesNode(bits[2], bits[4])
  else:
    raise template.TemplateSyntaxError("'%s' tag takes four arguments" % bits[0])