from django.conf import settings
from django.contrib.contenttypes.models import ContentType

"""
Simply re-saves all objects from models listed in settings.AGGREGATOR_MODELS. Since the aggregator
app is now following these models, it will register each item as it is re-saved. The purpose of this
script is to register content in your database that existed prior to installing the aggregator app.
"""

for item in settings.AGGREGATOR_MODELS:
  app_label     = item['model'].split('.')[0]
  model         = item['model'].split('.')[1]
  content_type  = ContentType.objects.get(app_label=app_label, model=model)
  model         = content_type.model_class()

  objects = model.objects.all()
  for object in objects:
    try:
      object.save()
    except:
      pass