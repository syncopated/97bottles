from django.template import add_to_builtins

add_to_builtins('django.contrib.markup.templatetags.markup')
add_to_builtins('django.contrib.humanize.templatetags.humanize')
add_to_builtins('django.templatetags.cache')

add_to_builtins('pagination.templatetags.pagination_tags')
add_to_builtins('tagging.templatetags.tagging_tags')
add_to_builtins('typogrify.templatetags.typogrify')
add_to_builtins('mailfriend.templatetags.mailfriend')

try:
  import PIL
  add_to_builtins('sorl.thumbnail.templatetags.thumbnail')
  add_to_builtins('savoy.core.template_utils.templatetags.thumbnail')
except:
  pass

add_to_builtins('savoy.core.template_utils.templatetags.template_utils')
add_to_builtins('savoy.core.template_utils.templatetags.comparison')
add_to_builtins('savoy.core.template_utils.templatetags.generic_content')
add_to_builtins('savoy.core.template_utils.templatetags.render_template_for')
add_to_builtins('savoy.core.template_utils.templatetags.tags')
add_to_builtins('savoy.core.template_utils.templatetags.feeds')