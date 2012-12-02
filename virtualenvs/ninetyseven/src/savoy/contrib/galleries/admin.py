from django.contrib import admin

from savoy.contrib.galleries.models import *

class GalleryPhotoInline(admin.TabularInline): 
  model = GalleryPhoto
  extra = 3
  raw_id_fields = ('photo',)

class GalleryVideoInline(admin.TabularInline): 
  model = GalleryVideo
  extra = 3
  raw_id_fields = ('video',)

class GalleryAudioInline(admin.TabularInline): 
  model = GalleryAudio
  extra = 3
  raw_id_fields = ('audio',)

class GalleryDocumentInline(admin.TabularInline): 
  model = GalleryDocument
  extra = 3
  raw_id_fields = ('document',)

class GalleryAdmin(admin.ModelAdmin):
  inlines = [GalleryPhotoInline, GalleryVideoInline, GalleryAudioInline, GalleryDocumentInline]
  prepopulated_fields = {'slug': ("title",)}
  list_display = ('title','date_published','source','date_created','photo_count','video_count','audio_count','document_count',)
  search_fields = ('title','description','tags',)

admin.site.register(Gallery, GalleryAdmin)