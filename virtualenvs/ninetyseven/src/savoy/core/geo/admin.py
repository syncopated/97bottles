from django.contrib import admin

from savoy.core.geo.models import *

class GeolocatedItemAdmin(admin.ModelAdmin):
  list_display = ('__unicode__','latitude', 'longitude', 'neighborhood', 'city',)
  list_filter = ('content_type',)
  raw_id_fields = ('city',)
  search_fields = ('city__city','neighborhood__name',)

admin.site.register(GeolocatedItem, GeolocatedItemAdmin)


class CityAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ("city", "state", "province", "country")}
  ordering = ('city',)
  list_display = ('city', 'state', 'province', 'country',)
  search_fields = ('city', 'state', 'province', 'country',)
  list_filter   = ('state', 'country',)

admin.site.register(City, CityAdmin)


class NeighborhoodAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}
  list_display = ('name','city',)
  search_fields = ('name',)
  raw_id_fields = ('city',)

admin.site.register(Neighborhood, NeighborhoodAdmin)


class PlaceTypeAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('plural_name',)}
  list_display = ('name',)
  search_fields = ('name',)

admin.site.register(PlaceType, PlaceTypeAdmin)


class PlaceAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('pre_name', 'name')}
  fieldsets = (
      (None, {
          'fields': ('pre_name', 'name', 'slug', 'nickname',)
      }),
      ('Location', {
          'fields': ('address1', 'address2', 'address_hint', 'neighborhood', 'city', 'zip_code',)
      }),
      ('Contact info', {
          'classes': ('collapse',),
          'fields': ('phone1', 'phone2', 'fax', 'website', 'email')
      }),
      ('About', {
          'classes': ('collapse',),
          'fields': ('description','is_public', 'is_defunct', 'place_types', 'accessibility','is_outdoors',)
      }),
      ('Tags', {
          'classes': ('collapse',),
          'fields': ('tags',)
      }),
  )
  list_display = ('name', 'address1', 'city',)
  list_filter = ('place_types', 'is_public','is_defunct',)
  search_fields = ('name','description',)
  radio_fields = {'accessibility': admin.HORIZONTAL}
  raw_id_fields = ('city',)

admin.site.register(Place, PlaceAdmin)