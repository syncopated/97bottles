from django.contrib import admin
from savoy.core.new.profiles.models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'gender', 'city')
    raw_id_fields = ('city',)

admin.site.register(Profile, ProfileAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('profile', 'service')
    list_filter = ('profile', 'service')
    
admin.site.register(Service, ServiceAdmin)

class LinkAdmin(admin.ModelAdmin):
    list_display = ('profile', 'title', 'url')
    
admin.site.register(Link, LinkAdmin)

admin.site.register(MobileProvider)
admin.site.register(ServiceType)