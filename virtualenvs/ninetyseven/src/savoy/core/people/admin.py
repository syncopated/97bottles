from django.contrib import admin

from savoy.core.people.models import *

class RoleInline(admin.TabularInline): 
  model = Role
  extra = 3

class BioHighlightInline(admin.TabularInline): 
  model = BioHighlight
  extra = 3

class PersonAdmin(admin.ModelAdmin):
  inlines = [RoleInline, BioHighlightInline]
  prepopulated_fields = {'slug': ("first_name","last_name","suffix")}
  list_display = ('full_name','first_name','last_name','user','organizations')
  search_fields = ('last_name','first_name','bio',)
  fieldsets = (
    ('Basics:', {
      'fields': ('salutation', 'first_name','middle_name', 'last_name','suffix','slug', 'user',),
    }),
    ('Details (optional):', {
      'fields': ('bio','photo',),
    }),
    ('Display Location (optional):', {
      'classes': 'collapse',
      'fields': ('home','work'),
    }),
    ('Contact (optional):', {
      'classes': 'collapse',
      'fields': ('home_phone','work_phone','mobile_phone','fax','home_email','work_email','personal_url','professional_url'),
    }),
    ('Categorization:', {
      'classes': 'collapse',
      'fields': ('tags',)
    }),
  )

admin.site.register(Person, PersonAdmin)