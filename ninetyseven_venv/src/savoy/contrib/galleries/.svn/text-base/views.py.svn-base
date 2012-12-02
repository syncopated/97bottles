import datetime, time

from django.http import Http404
from django.shortcuts import get_object_or_404

from savoy.contrib.galleries.models import *
from savoy.core.media.models import *

def gallery_detail(request, slug, paginate_by=30, page=None, allow_empty=True):
  from django.views.generic.list_detail import object_detail
  
  gallery = get_object_or_404(Gallery, slug=slug)
  
  extra_context = { 
    'photo_list': gallery.galleryphoto_set.all(),
  }
  
  return object_detail(
    request, 
    queryset = Gallery.objects.all(),
    template_name = 'galleries/gallery_detail.html',
    template_object_name='gallery',
    slug_field = 'slug',
    slug = slug,
    extra_context = extra_context,
  )   
  
  

def gallery_photo_detail(request, year, month, day, photo_slug, gallery_slug, month_format='%b', day_format='%d'):
  from django.views.generic.date_based import object_detail
  
  try:
    gallery = Gallery.objects.get(slug=gallery_slug)
    date = datetime.date(*time.strptime(year+month+day, '%Y'+month_format+day_format)[:3])
    photos_from_date = Photo.objects.filter(date_published__range = (datetime.datetime.combine(date, datetime.time.min), datetime.datetime.combine(date, datetime.time.max)))
    photo = photos_from_date.get(slug = photo_slug,)
  except:
    raise Http404
  try:
    galleryphoto = GalleryPhoto.objects.get(gallery=gallery, photo=photo)
  except AssertionError:
    # If the same photo is in a gallery twice, we'll get an exception. In that case,
    # use filter and take the first item off the list. This is not perfect, but it's
    # better than a 500 error.
    galleryphoto = GalleryPhoto.objects.filter(gallery=gallery, photo=photo)[0]
  
  extra_context={ 
    'gallery' : gallery,
    'galleryphoto' : galleryphoto,
  }
  
  return object_detail(
    request, 
    queryset = photos_from_date,
    year = year,
    month = month,
    day = day,
    date_field = 'date_published',
    slug_field = 'slug',
    slug = photo_slug,
    template_name = 'media/photos/photo_detail.html',
    template_object_name='photo',
    extra_context=extra_context,
  )
