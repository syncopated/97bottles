from django import template

from savoy.core.people.models import *

register = template.Library()

class PeopleListNode(template.Node):
    def __init__(self, varname):
        self.varname = varname
    
    def render(self, context):
      try:
        people_list = Person.objects.all()
        context[self.varname] = people_list
      except:
        pass
      return ''

@register.tag
def get_people_list(parser, token):
    """
    Retrieves a list of all people in the system.
    
    Syntax::
    
        {% get_people_list as people_list %}
        
    """
    bits = token.contents.split()
    return PeopleListNode(bits[2])