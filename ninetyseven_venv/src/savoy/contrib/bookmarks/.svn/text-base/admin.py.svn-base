from django.contrib import admin

from savoy.contrib.bookmarks.models import *

class BookmarkAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('title',)}
  list_display = ('title','date_published', 'source','rating',)
  search_fields = ('title','description',)
  fieldsets = (
      ('Basic (required)', {
          'fields': ('url','title','slug','date_published',)
      }),
      ('Additional (optional)', {
          'fields': ('description',)
      }),
      ('Categorization (optional)', {
          'fields' : ('tags',)
      }),
  )

admin.site.register(Bookmark, BookmarkAdmin)