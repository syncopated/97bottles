from savoy.utils.path import append_third_party_path
append_third_party_path()

import datetime
import flickrapi

from django.conf import settings
from django.template.defaultfilters import slugify

from savoy.contrib.galleries.models import *
from savoy.core.media.models import *
from savoy.core.media.importers.flickr import *

flickr = flickrapi.FlickrAPI(settings.FLICKR_API_KEY, settings.FLICKR_API_SECRET)

def create_or_update_galleryphoto_for_photoset_photo(gallery, photo):
  try:
    galleryphoto = GalleryPhoto.objects.get(gallery=gallery, photo=photo)
  except:
    galleryphoto = GalleryPhoto(gallery=gallery, photo=photo)
    galleryphoto.save()

def create_or_update_gallery_for_photoset(photoset):
  try:
    gallery = FlickrPhotoset.objects.get(flickr_photoset_id=photoset['id']).gallery
  except:
    gallery = Gallery()
    gallery.date_published = datetime.datetime.now()
  gallery.title = photoset.title[0].elementText
  gallery.slug = slugify(photoset.title[0].elementText)
  gallery.description = photoset.description[0].elementText
  gallery.status = 2
  gallery.save()
  return gallery

def create_or_update_photosets_for_user(user_id, flickr_user):
  photosets = flickr.photosets_getList(user_id=user_id).photosets[0].photoset
  
  for photoset in photosets:
    try:
      flickr_photoset = FlickrPhotoset.objects.get(flickr_photoset_id=photoset['id'])
      for galleryphoto in flickr_photoset.gallery.galleryphoto_set.all():
        galleryphoto.delete()
    except:
      flickr_photoset = FlickrPhotoset(flickr_photoset_id=photoset['id'])
    flickr_photoset.gallery = create_or_update_gallery_for_photoset(photoset=photoset)
    flickr_photoset.owner = flickr_user
    flickr_photoset.secret = photoset['secret']
    flickr_photoset.server_id = int(photoset['server'])
    flickr_photoset.photo_count = int(photoset['photos'])
    try:
      flickr_photoset.primary_photo = FlickrPhoto.objects.get(flickr_photo_id=int(photoset['primary'])).photo
    except:
      flickr_photoset.primary_photo = None
    flickr_photoset.save()
      
    photos = flickr.photosets_getPhotos(photoset_id=photoset['id']).photoset[0].photo
    for photo in photos:
      photo_id = photo['id']
      try:
        savoy_photo = FlickrPhoto.objects.get(flickr_photo_id=photo_id).photo
        create_or_update_galleryphoto_for_photoset_photo(gallery=flickr_photoset.gallery, photo=savoy_photo)
      except:
        try:
          savoy_photo = create_or_update_flickr_photo(photo_id=photo_id)
          create_or_update_galleryphoto_for_photoset_photo(gallery=flickr_photoset.gallery, photo=savoy_photo)
        except:
          pass
    flickr_photoset.gallery.save()

def update():
  # Get the person info
  user_id = settings.FLICKR_USERID

  # Save the flickr person as a Savoy FlickrUser object
  flickr_user = create_or_update_flickr_user(user_id=user_id)

  # Get the photos for this person
  create_or_update_photosets_for_user(user_id=user_id, flickr_user=flickr_user)

if __name__ == '__main__':
    update()