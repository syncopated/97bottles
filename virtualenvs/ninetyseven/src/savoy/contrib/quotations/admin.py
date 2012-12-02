from django.contrib import admin

from savoy.contrib.quotations.models import *

class QuotationAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ("author","quote")}
  list_display = ('quote','author','author_affiliation',)
  search_fields = ('quote','author',)

admin.site.register(Quotation, QuotationAdmin)