from django.contrib import admin

from savoy.contrib.code_samples.models import *


class LanguageAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}
  list_display = ('name','slug')
  search_fields = ('name','slug')

admin.site.register(Language, LanguageAdmin)


class CodeSampleAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('title',)}
  list_display = ('title','language')
  search_fields = ('title','language','description')

admin.site.register(CodeSample, CodeSampleAdmin)