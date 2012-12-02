from django.contrib import admin

from savoy.contrib.podcasts.models import *

class PodcastAudioInline(admin.TabularInline): 
  model = PodcastAudio
  extra = 1

class PodcastVideoInline(admin.TabularInline): 
  model = PodcastVideo
  extra = 1

class ShowAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ("name",)}
  list_display  = ('name','slug')
  search_fields = ('name',)
  raw_id_fields = ('hosts',)
admin.site.register(Show, ShowAdmin)

class EpisodeAdmin(admin.ModelAdmin):
  inlines = [PodcastVideoInline, PodcastAudioInline,]
  prepopulated_fields = {'slug': ("title",)}
  list_display  = ('title','show', 'date_published')
  search_fields = ('title','show','description',)
admin.site.register(Episode, EpisodeAdmin)