from django.contrib import admin

from savoy.contrib.events.models import *

class OneOffEventTimeInline(admin.TabularInline): 
  model = OneOffEventTime
  extra = 3

class AllDayEventTimeInline(admin.TabularInline): 
  model = AllDayEventTime
  extra = 3

class WeeklyEventTimeInline(admin.TabularInline): 
  model = WeeklyEventTime
  extra = 3

class MonthlyEventTimeInline(admin.TabularInline): 
  model = MonthlyEventTime
  extra = 3

class EventAdmin(admin.ModelAdmin):
  inlines = [OneOffEventTimeInline, AllDayEventTimeInline, WeeklyEventTimeInline, MonthlyEventTimeInline]
  prepopulated_fields = {'slug': ("title",)}
  list_display = ('title','short_description', 'added_by', 'date_created','start_time',)
  search_fields = ('title','short_description','description','tags',)
  date_hierarchy  = 'date_published'
  list_filter=('date_created','date_published',)
  fieldsets = (
      ('Basics:', {'fields': ('title', 'slug', 'date_published','added_by', 'short_description', 'description', 'event_url')}),
      ('People and places:', {'fields': ('places', 'organizers', 'sponsors', 'individual_organizers', 'individual_sponsors',)}),
      ('Categorization:', {'fields': ('tags',)}),
      ('Cost and tickets:', {'fields': ('cost_high','cost_low','ticket_url',)}),
  )

admin.site.register(Event, EventAdmin)