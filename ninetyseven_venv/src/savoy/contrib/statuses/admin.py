from django.contrib import admin

from savoy.contrib.statuses.models import *

class StatusAdmin(admin.ModelAdmin):
  list_display            = ('body','twitter_user','date_published')
  search_fields           = ('body',)

admin.site.register(Status, StatusAdmin)