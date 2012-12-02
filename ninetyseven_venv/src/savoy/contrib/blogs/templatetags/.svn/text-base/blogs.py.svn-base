from django import template

from savoy.contrib.blogs.models import Blog, Entry

register = template.Library()

class EntryYearListNode(template.Node):
    def __init__(self, varname):
        self.varname = varname
    
    def render(self, context):
      try:
        entries = Entry.objects.all()
        year_list = entries.dates('date_published', 'year')[::-1]
        context[self.varname] = year_list
      except:
        pass
      return ''
      
@register.tag
def get_entry_year_list(parser, token):
    """
    Retrieves the a list of dates representing years that contain blog entries..
    
    Syntax::
    
        {% get_entry_year_list as date_list %}
        
    """
    bits = token.contents.split()
    return EntryYearListNode(bits[2])

class LatestEntriesNode(template.Node):
    def __init__(self, blog_slug, num, varname, manager=None):
        self.blog_slug, self.num, self.varname, self.manager = blog_slug, int(num), varname, manager
    
    def render(self, context):
      manager = self.manager
      try:
        if self.manager:
          entries = getattr(Entry, self.manager).filter(blogs__slug=self.blog_slug).order_by('-date_published')[:self.num]
        else:
          entries = Entry.objects.filter(blogs__slug=self.blog_slug).order_by('-date_published')[:self.num]
        context[self.varname] = entries
      except:
        pass
      return ''

@register.tag
def get_latest_entries(parser, token):
    """
    Retrieves the latest ``num`` Entries from a given Blog, and stores them in a context variable.
    
    Syntax::
    
        {% get_latest_entries [blog-slug] [num] as [varname] (with manager [manager_name]) %}
    
    Example::
    
        {% get_latest_entries redhot 5 as latest_redhot_entries with manager live_entries %}
    
    """
    bits = token.contents.split()
    try:
      return LatestEntriesNode(bits[1], bits[2], bits[4], bits[7])
    except:
      return LatestEntriesNode(bits[1], bits[2], bits[4])



class FeaturedBlogsNode(template.Node):
    def __init__(self, varname):
      self.varname = varname

    def render(self, context):
      try:
        blogs = Blog.objects.filter(featured=True).order_by('-date_created')
        context[self.varname] = blogs
      except:
        pass
      return ''

@register.tag
def get_featured_blogs(parser, token):
    """
    Retrieves the Blogs marked as "featured", and stores them in a context variable.

    Syntax::

        {% get_featured_blogs as [varname] %}

    Example::

        {% get_featured_blogs as featured_blog_list %}

    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    if bits [1] != 'as':
        raise template.TemplateSyntaxError("first argument to '%s' tag must be 'as'" % bits[0])
    return FeaturedBlogsNode(bits[2])



class FeaturedEntriesNode(template.Node):
    def __init__(self, num, varname):
      self.varname, self.num  = varname, num

    def render(self, context):
      try:
        entries = Entry.objects.filter(featured=True).order_by('-date_created')
        context[self.varname] = entries
      except:
        pass
      return ''

@register.tag
def get_featured_entries(parser, token):
    """
    Retrieves the requested number of Entries marked as "featured", and stores them in a context variable.

    Syntax::

        {% get_featured_entries 10 as [varname] %}

    Example::

        {% get_featured_entries 10 as featured_blog_list %}

    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    if bits [2] != 'as':
        raise template.TemplateSyntaxError("second argument to '%s' tag must be 'as'" % bits[0])
    return FeaturedEntriesNode(bits[1], bits[3])
    
    
    
class GetBlogBySlugNode(template.Node):
    def __init__(self, slug, varname):
      self.varname, self.slug  = varname, slug

    def render(self, context):
      try:
        blog = Blog.objects.get(slug=self.slug)
        context[self.varname] = blog
      except:
        pass
      return ''

@register.tag
def get_blog_by_slug(parser, token):
    """
    Retrieves the requested blog by it's slug and assigns it to a context variable.

    Syntax::

        {% get_blog_by_slug [slug] as [varname] %}

    Example::

        {% get_blog_by_slug "redhot" as redhot_blog %}

    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    if bits [2] != 'as':
        raise template.TemplateSyntaxError("second argument to '%s' tag must be 'as'" % bits[0])
    return GetBlogBySlugNode(bits[1], bits[3])