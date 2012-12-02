from django.contrib import admin

from savoy.core.profiles.models import *

class ServiceInline(admin.TabularInline): 
  model = Service
  extra = 3

class WebsiteInline(admin.TabularInline): 
  model = Website
  extra = 3

class ProfileAdmin(admin.ModelAdmin):
  inlines = [ServiceInline, WebsiteInline]
  list_display      = ('user','gender','birth_date','mobile_number','mobile_carrier')
  list_filter       = ('gender','mobile_carrier')
  search_fields     = ('user',)
  radio_fields      = {'gender': admin.HORIZONTAL}

admin.site.register(Profile, ProfileAdmin)


class MobileCarrierAdmin(admin.ModelAdmin):
  pass
  
admin.site.register(MobileCarrier, MobileCarrierAdmin)


class ServiceTypeAdmin(admin.ModelAdmin):
  pass
  
admin.site.register(ServiceType, ServiceTypeAdmin)
