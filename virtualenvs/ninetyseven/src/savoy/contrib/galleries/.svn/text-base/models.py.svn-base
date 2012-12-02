from django.db import models

from tagging.fields import TagField
from savoy.core.constants import STATUS_CHOICES
from savoy.core.media.models import *

class Gallery(models.Model):
  """A Gallery is a set of content items, such as photos or videos."""
  title               = models.CharField(max_length=250)
  slug                = models.SlugField(unique=True, help_text='The slug is a URL-friendly version of the tag. It is auto-populated.')
  description         = models.TextField(blank=True, help_text='Add a caption for the gallery.')
  tags                = TagField(help_text="Add tags for this gallery.")
  
  date_published      = models.DateTimeField(default=datetime.datetime.now, help_text="Enter the date and time this gallery should be available on the site.")
  date_created        = models.DateTimeField(default=datetime.datetime.now, editable=False)
  
  status              = models.IntegerField(help_text="Select the status of this gallery.", choices=STATUS_CHOICES, default=2)
  
  class Meta:
    verbose_name_plural = "Galleries"

  def __str__(self):
    return self.title
  
  def save(self, force_insert=False, force_update=False):
    # Kind of ugly hack to account for the fact that Flickr doesn't provide creation dates for its photosets.
    # We'll just use the date_published of the oldest photo the set contains as the date_published for the gallery.
    if self.flickr_photoset and self.galleryphoto_set.all():
      from django.template.defaultfilters import dictsort
      galleryphotos = self.galleryphoto_set.all()
      photos = []
      for gp in galleryphotos:
        photos.append(gp.photo)
      oldest_photo = dictsort(photos, 'date_published')[0]
      self.date_published = oldest_photo.date_published
    super(Gallery, self).save(force_insert=force_insert, force_update=force_update)
  
  @permalink
  def get_absolute_url(self):
    return ('gallery_detail', None, {'slug': self.slug})

  @property
  def photo_count(self):
    return self.galleryphoto_set.all().count()

  @property
  def video_count(self):
    return self.galleryvideo_set.all().count()
  
  @property
  def audio_count(self):
    return self.galleryaudio_set.all().count()

  @property
  def document_count(self):
    return self.gallerydocument_set.all().count()
  
  @property
  def flickr_photoset(self):
    try:
      return FlickrPhotoset.objects.get(gallery=self)
    except:
      return None
  
  @property
  def source(self):
    if self.flickr_photoset:
      return 'flickr'
    else:
      return 'local'
    
  
  def contains_photos(self):
    if self.galleryphoto_set.all:
      return True
    else:
      return False

  def contains_videos(self):
    if self.galleryvideo_set.all:
      return True
    else:
      return False

  def contains_audio(self):
    if self.galleryaudio_set.all:
      return True
    else:
      return False

  def contains_documents(self):
    if self.gallerydocument_set.all:
      return True
    else:
      return False

class GalleryPhoto(models.Model):
  """A GalleryPhoto establishes the relationship between a piece a Photo and a Gallery. """
  gallery             = models.ForeignKey(Gallery)
  photo               = models.ForeignKey(Photo)

  @permalink
  def get_absolute_url(self):
    y = self.photo.date_published.strftime("%Y").lower()
    m = self.photo.date_published.strftime("%b").lower()
    d = self.photo.date_published.strftime("%d").lower()
    s = str(self.photo.slug)
    g = str(self.gallery.slug)
    return ('gallery_photo_detail', None, {'year': y, 'month': m, 'day': d, 'photo_slug': s, 'gallery_slug': g})

  def _get_adjacent_photo(self, direction):
    photos = list(self.gallery.galleryphoto_set.all())
    num_photos = len(photos)-1
    current_photo = photos.index(self)
    photo = None
    if direction == 'next':
      if current_photo != num_photos:
        photo = photos[current_photo+1]
    elif direction == 'previous':
      if current_photo != 0:
        photo = photos[current_photo-1]
    return photo
      
  def get_next_galleryphoto(self):
    return self._get_adjacent_photo(direction='next')

  def get_previous_galleryphoto(self):
    return self._get_adjacent_photo(direction='previous')

  class Meta:
    verbose_name_plural = "Photos in gallery"
  
  def __str__(self):
    return self.photo.__str__() + ' in ' + self.gallery.__str__()

class GalleryVideo(models.Model):
  """A GalleryVideo establishes the relationship between a piece a Video and a Gallery. """
  gallery             = models.ForeignKey(Gallery)
  video               = models.ForeignKey(Video)

  class Meta:
    verbose_name_plural = "Videos in gallery"

  def __str__(self):
    return self.video.__str__() + ' in ' + self.gallery.__str__()

class GalleryAudio(models.Model):
  """A GalleryAudio establishes the relationship between a piece an Audio and a Gallery. """
  gallery             = models.ForeignKey(Gallery)
  audio               = models.ForeignKey(Audio)

  class Meta:
    verbose_name_plural = "Audio files in gallery"

  def __str__(self):
    return self.audio.__str__() + ' in ' + self.gallery.__str__()

class GalleryDocument(models.Model):
  """A GalleryDocument establishes the relationship between a piece a Document and a Gallery. """
  gallery             = models.ForeignKey(Gallery)
  document            = models.ForeignKey(Document)

  class Meta:
    verbose_name_plural = "Documents in gallery"

  def __str__(self):
    return self.document.__str__() + ' in ' + self.gallery.__str__()


class FlickrPhotoset(models.Model):
  gallery         = models.ForeignKey(Gallery)
  owner           = models.ForeignKey(FlickrUser)
  flickr_photoset_id = models.CharField(max_length=250, unique=True, primary_key=True)
  server_id       = models.PositiveSmallIntegerField()
  primary_photo   = models.ForeignKey(Photo, blank=True, null=True)
  photo_count     = models.PositiveIntegerField()
  secret          = models.CharField(max_length=250)
  date_created    = models.DateTimeField(default=datetime.datetime.now, editable=False)

  def __unicode__(self):
    return str(self.flickr_photoset_id) + ": " + self.gallery.title
    
