from django.contrib import admin

from savoy.contrib.aggregator.models import *

class ContentItemAdmin(admin.ModelAdmin):
  list_filter = ['content_type']
  list_display = ('__unicode__', 'timestamp', 'content_type')
  
admin.site.register(ContentItem, ContentItemAdmin)