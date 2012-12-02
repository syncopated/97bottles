from django.contrib import admin

from savoy.contrib.inlines.models import *

class InlineTypeAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}
  list_display = ('name','content_type','slug','template',)
  search_fields = ('name','content_type','slug','template',)

admin.site.register(InlineType, InlineTypeAdmin)