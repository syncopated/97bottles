from django.template import add_to_builtins
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from savoy.contrib.aggregator.models import ContentItem

add_to_builtins('savoy.contrib.aggregator.templatetags.aggregator')
add_to_builtins('savoy.contrib.aggregator.templatetags.calendar')

for item in settings.AGGREGATOR_MODELS:
  try:
    app_label     = item['model'].split('.')[0]
    model         = item['model'].split('.')[1]
    content_type  = ContentType.objects.get(app_label=app_label, model=model)
    model         = content_type.model_class()
    ContentItem.objects.follow_model(model)
  except ContentType.DoesNotExist:
    pass