from django import template
from django.template import Context, Template, loader, Library, Node

from savoy.contrib.inlines.models import *

register = Library()

def do_inlines(value, render_content=False):
   """ 
   Processes inlines for a string of text (such as a blog post). If 
   render_content is True, will return the full blog post HTML, with inlines
   rendered through their templates. If rendered_content is false, will return
   a list of inline objects.
   """
   from BeautifulSoup import BeautifulStoneSoup, Tag
   
   # Parse the entry content, passing BeautifulStoneSoup our inline tag (plus the regular HTML ones) as self-closing.
   content = BeautifulStoneSoup(value, selfClosingTags=['br' , 'hr', 'input', 'img', 'meta','spacer', 'link', 'frame', 'base','inline'])
   
   # Set up the inline_objects list.
   inline_objects = []

   # If rendered_content is true, then we want the entire rendered HTML as a result.
   if render_content == True:
     
    # Look for 'inline' elements, and itterate through them.
    for inline in content.findAll('inline'):
      # Get the html from the template for each inline element

      html_dict = process_inline(inline, html=True)
      try:
        inline_object_details = html_dict["inline_object_details"]
      except:
        return html_dict
      # Add the details of this inline to the inline_objects array.
      inline_object_details = html_dict["inline_object_details"]
      inline_html = html_dict["inline_html"]
      inline_objects.append(html_dict["inline_object_details"])
      # Add a new div tag to the tree, and then replace our inline tag with it, instead.
      inline_tag = Tag(content, "div", [("id", inline_object_details['html_id']),("class", inline_object_details['html_class'])])
      inline_tag.insert(0, inline_html)
      inline.replaceWith(inline_tag)

      
    # Render out the final HTML for the blog post.
    final_html = content.renderContents()
    return final_html
       
   # If render_content is false, then we just want a list of the objects themselves.
   else:
      
      # Look for 'inline' elements, and itterate through them.
      for inline in content.findAll('inline'):
        # Add the details of this inline to the inline_objects list.
        processed_inline = process_inline(inline, html=False)
        inline_objects.append(processed_inline['object'])
      
      # Return the final list of inline objects.
      return inline_objects


def process_inline(inline, html=True):
    """
    Processes an individual inline by finding its model and getting the desired object.
    If html is true, will return the inline HTML for the object, as rendered through
    the inline type's template. If html is false, will simply return the object.
    """
    # Try to find an encode the various attributes of an inline. Set up the HTML classes.
    html_classes = ['inline',]
    
    try:
      object_type = inline['type']
      html_classes.append("inline-type-" + object_type)
    except:
      raise Exception
    try:
      object_id = int(inline['id'])
      html_classes.append("inline-id-" + str(object_id))
    except:
      raise Exception

    try:
      object_class = inline['class']
      html_classes.append(object_class)
    except:
      object_class = None

    # Then, piece together the HTML classes for this inline
    html_class = " ".join(html_classes)
    html_id = object_type + '-' + str(object_id)
                                                                                                                                                     
    # Try to find the inline type in the InlineTypes.
    try:
      inline_type = InlineType.objects.get(slug=object_type)
    except:
      return "<p><strong>Inline object type " + object_type + " not found</strong></p>"
    
    try:
      content_type = inline_type.content_type
      from django.db.models import get_model
      inline_model = content_type.model_class()
      inline_object = inline_model._default_manager.get(id=object_id)
    except:
      return "<p><strong>Inline object id " + str(object_id) + " not found</strong></p>"
    
      
    # Create a dictionary of all the details of this inline.
    inline_object_details = {
      'object_type': inline_type,
      'object': inline_object,
      'object_id': object_id,
      'model': inline_model,
      'html_class': html_class,
      'html_id': html_id,
    }
    
    # If html is true, use the inline_object_details dictionary and
    # render our context through the inline's template. Return a dictionary
    # that inludes the rendered HTML as well as some other useful bits like
    # the CSS class and the inline object's ID.
    if html==True:
      template = loader.get_template(inline_type.template)
      context = Context(inline_object_details)
      inline_html = template.render(context)
      return { 
        'inline_object_details': inline_object_details, 
        'inline_html': inline_html,
      }
    
    # If html is False, just return the found object details dictionary.
    if html==False:
      return inline_object_details

@register.filter
def inlines(value):
  """Processes inlines for content, returning full content with inline items inserted."""
  return do_inlines(value, render_content=True)
  
@register.filter
def find_inlines(value):
  """Processes inlines for content, returning a list of all the inline objects."""
  return do_inlines(value, render_content=False)