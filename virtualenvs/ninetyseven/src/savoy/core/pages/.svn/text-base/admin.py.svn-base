from django.contrib import admin

from savoy.core.pages.models import *

class PageAdmin(admin.ModelAdmin):
  list_display = ('url','title','pub_date','status',)
  search_fields = ('url','title','primary_content','secondary_content',)
  date_hierarchy  = 'pub_date'
  list_filter     = ('pub_date','status','markup_language',)

admin.site.register(Page, PageAdmin)
admin.site.register(PageTemplate)