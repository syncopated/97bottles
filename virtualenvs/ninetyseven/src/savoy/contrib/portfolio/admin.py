from django.contrib import admin

from savoy.contrib.portfolio.models import *

class MediumAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ("name",)}

admin.site.register(Medium, MediumAdmin)


class DisciplineAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ("name",)}

admin.site.register(Discipline, DisciplineAdmin)


class TestimonialAdmin(admin.ModelAdmin):
  pass

admin.site.register(Testimonial, TestimonialAdmin)


class ImageAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ("title",)}


class RoleInline(admin.TabularInline): 
  model = Role
  extra = 10


class ImageInline(admin.StackedInline):
  model = Image
  extra = 1
  prepopulated_fields = {'slug': ("title",)}


class ProjectAdmin(admin.ModelAdmin):
  inlines = [ImageInline, RoleInline]
  prepopulated_fields = {'slug': ("title",)}
  list_display = ('title', 'client', 'date_published', 'date_completed',)
  search_fields = ['title', 'summary','description']
  list_filter = ['client', 'mediums', 'date_completed', 'date_published', 'in_development', 'is_public']
  fieldsets = (
      (None, {'fields': ('title', 'slug', 'url', 'summary', 'description','date_published',)}),
      ('Metadata', {'fields': ('client', 'mediums', 'disciplines', 'date_completed','is_public', 'in_development')}),
  )

admin.site.register(Project, ProjectAdmin)