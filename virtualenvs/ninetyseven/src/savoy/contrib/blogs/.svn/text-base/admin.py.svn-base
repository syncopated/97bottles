from django.contrib import admin

from savoy.contrib.blogs.models import *

class EntryAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('title',)}
  date_hierarchy  = 'date_published'
  list_display    = ('title', 'date_published','author', 'status', 'enable_comments')
  list_filter     = ('date_published','status')
  search_fields   = ('title', 'intro', 'summary','body','body_extended')
  fieldsets = (
    ('Meta:', {'fields': ('author', 'blogs','posted_from','title', 'slug', 'date_published',)}),
    ('Entry content:', {'fields': ('intro', 'body','body_extended','summary')}),
    ('Categorization:', {'fields': ('tags',)}),
    ('Options:', {'fields': ('status','markup_language','process_inlines','enable_comments','featured',)}),
  )
  ordering = ['-date_published']

admin.site.register(Entry, EntryAdmin)

class BlogAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('title',)}
  list_display = ('title','slug','date_created','featured')
  search_fields = ('title','slug')
  
admin.site.register(Blog, BlogAdmin)