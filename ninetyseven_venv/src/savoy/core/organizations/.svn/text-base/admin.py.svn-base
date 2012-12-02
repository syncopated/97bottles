from django.contrib import admin

from savoy.core.organizations.models import *

class OrganizationAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ("pre_name","name")}
  list_display = ('name','url',)
  search_fields = ('name','description',)
  fieldsets = (
    ('Basics:', {
      'fields': ('pre_name', 'name','slug','industry'),
    }),
    ('Details (optional):', {
      'classes': ('collapse',),
      'fields': ('description',),
    }),
    ('Locations:', {
      'fields': ('locations',),
    }),
    ('Contact (optional):', {
      'classes': ('collapse',),
      'fields': ('phone1','phone2','fax','email','url'),
    }),
    ('Categorization:', {
      'classes': ('collapse',),
      'fields': ('tags',)
    }),
  )

admin.site.register(Organization, OrganizationAdmin)


class IndustryAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}

admin.site.register(Industry, IndustryAdmin)