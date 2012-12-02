from django.contrib import admin

from savoy.contrib.comments.models import *

class CommentAdmin(admin.ModelAdmin):
  list_display                  = ('author_name', 'person', 'author_email_address', 'date_submitted', 'parent_object', 'source','approved',)
  list_filter                   = ('person', 'date_submitted', 'approved', 'featured','trollish','content_type',)
  date_hierarchy                = 'date_submitted'
  search_fields                 = ('body', 'person__user__username', 'author_name', 'author_email_address', 'author_ip_address')

admin.site.register(Comment, CommentAdmin)


class NameBlacklistItemAdmin(admin.ModelAdmin):
  pass
  
admin.site.register(NameBlacklistItem, NameBlacklistItemAdmin)


class EmailBlacklistItemAdmin(admin.ModelAdmin):
  pass
  
admin.site.register(EmailBlacklistItem, EmailBlacklistItemAdmin)


class IPBlacklistItemAdmin(admin.ModelAdmin):
  pass
  
admin.site.register(IPBlacklistItem, IPBlacklistItemAdmin)


class URLBlacklistItemAdmin(admin.ModelAdmin):
  pass
  
admin.site.register(URLBlacklistItem, URLBlacklistItemAdmin)


class EmailWhitelistItemAdmin(admin.ModelAdmin):
  pass
  
admin.site.register(EmailWhitelistItem, EmailWhitelistItemAdmin)