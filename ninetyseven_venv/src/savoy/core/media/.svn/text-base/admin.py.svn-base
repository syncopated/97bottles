from django.contrib import admin

from savoy.core.media.models import *

class PhotoAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('title',)}
  list_display = ('title','date_created', 'date_published','source','_admin_thumbnail','is_geolocated',)
  list_filter = ('date_created',)
  list_select_related = True
  search_fields = ('title', 'description',)
  raw_id_fields = ('photographer','organization',)
  date_hierarchy = 'date_created'
  fieldsets = (
      ('Upload photo (required)', {
          'fields': ('image',)
      }),
      ('Photo info (optional)', {
          'fields': ('title', 'slug', 'photographer','organization','copyright','date_created', 'description', 'tags')
      }),
  )

admin.site.register(Photo, PhotoAdmin)


class VideoAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('title',)}
  radio_fields = {'video_type': admin.HORIZONTAL}
  raw_id_fields = ('places_recorded','places_in_video','directors','producers','writers','videographers','organizations','people_in_video',)

admin.site.register(Video, VideoAdmin)


class AudioAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('title',)}
  radio_fields = {'audio_type': admin.HORIZONTAL}
  raw_id_fields = ('places_recorded','directors','producers','writers','audio_engineers','organizations','people_in_audio',)
  

admin.site.register(Audio, AudioAdmin)


class DocumentAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('title',)}

admin.site.register(Document, DocumentAdmin)


class EmbeddedMediaTypeAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}
  list_display = ('name',)
  search_fields = ('name',)

admin.site.register(EmbeddedMediaType, EmbeddedMediaTypeAdmin)


class EmbeddedMediaAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('title',)}
  list_display = ('title','type','date_published')
  search_fields = ('title','description','tags','type','embed_code')

admin.site.register(EmbeddedMedia, EmbeddedMediaAdmin)