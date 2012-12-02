from django.contrib import admin

from ninetyseven.apps.beers.models import *

class BreweryAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}
  list_display    = ('name','type','city','date_created','created_by')
  raw_id_fields   = ('city',)
  search_fields = ('name',)
  save_on_top     = True

class BeerAdmin(admin.ModelAdmin):
  search_fields = ('name',)
  prepopulated_fields = {'slug': ('name',)}
  list_display    = ('name', 'brewery','variety','rating','interestingness','date_created','created_by')
  save_on_top     = True
  list_filter     = ('top_rated','staff_favorite','womens_favorite','mens_favorite','color',)

class BeerColorAdmin(admin.ModelAdmin):
  list_display    = ('srm','ebc','example','color')

class VesselImageInline(admin.TabularInline):
  model = VesselImage
  extra = 10
  
class VesselAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}
  inlines = [VesselImageInline]
  
class UserInfoAdmin(admin.ModelAdmin):
  list_display    = ('user', 'contribution_score')

admin.site.register(Brewery, BreweryAdmin)
admin.site.register(BreweryType, prepopulated_fields = {'slug': ('name',)})
admin.site.register(BeerColor, BeerColorAdmin)
admin.site.register(Batch, prepopulated_fields = {'slug': ('name',)})
admin.site.register(Beer, BeerAdmin)
admin.site.register(Vessel, VesselAdmin)
admin.site.register(VesselImage)
admin.site.register(ServingType, prepopulated_fields = {'slug': ('name',)})
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(UserBeerScore)
admin.site.register(UserRecommendation)