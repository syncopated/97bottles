from django.contrib import admin

from ninetyseven.apps.reviews.models import *

class ReviewAdmin(admin.ModelAdmin):
  list_display    = ('created_by','beer','rating','vessel','serving_type','city','date_created')
  raw_id_fields   = ('city',)
  search_fields   = ('comment',)
  

admin.site.register(Review, ReviewAdmin)