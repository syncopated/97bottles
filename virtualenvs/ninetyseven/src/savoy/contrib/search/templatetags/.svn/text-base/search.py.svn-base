from django.template import Library, Context, loader

register = Library()

@register.simple_tag
def render_search_results(results):
  template_base     = "search/snippets/"
  html              = []
  for item in results:
    app_label       = item['model'].split('.')[0]
    model           = item['model'].split('.')[1]
    template_path   = template_base + item['model'] + ".html"
    template        = loader.get_template(template_path)
    context         = Context({ model:item['object'] })
    item_html       = unicode(template.render(context))
    html.append(item_html)
  return "\n".join(html)