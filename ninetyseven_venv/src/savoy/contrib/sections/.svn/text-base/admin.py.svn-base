from django.contrib import admin

from savoy.contrib.sections.models import *

class SectionAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ("title",)}
  list_display    = ('title', 'slug')
  search_fields   = ('title',)
  filter_horizontal = ('tags',)

admin.site.register(Section, SectionAdmin)