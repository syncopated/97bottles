import datetime

import simplejson
import EXIF
from django.conf import settings
from django.db import models
from django.db.models import signals
from django.db.models import permalink
from django.contrib.auth.models import User
from django.utils.encoding import smart_unicode, force_unicode
from django.contrib.contenttypes.models import ContentType
import tagging
from tagging.fields import TagField
from tagging.models import Tag

from savoy.core.people.models import Person
from savoy.core.geo.models import Place, GeolocatedItem
from savoy.core.organizations.models import Organization
from savoy.core.constants import VIDEO_TYPE_CHOICES, AUDIO_TYPE_CHOICES, DOC_TYPE_CHOICES
from savoy.core.media.managers import *

class Photo(models.Model):
    title               = models.CharField(max_length=250, help_text="Enter the title of this photo.")
    slug                = models.SlugField(max_length=200, unique_for_date="date_published", help_text='The slug is a URL-friendly version of the title. It is auto-populated.')
    description         = models.TextField(blank=True, help_text='Add a caption for the photo.')
    tags                = TagField(help_text="Add tags for this photo.")
    image               = models.ImageField(upload_to='photo/%Y/%m/%d', width_field='image_width', height_field='image_height', blank=True, help_text='Should be JPEG format. Larger pixel sizes are better.')
    image_width         = models.IntegerField(blank=True, null=True, editable=False)
    image_height        = models.IntegerField(blank=True, null=True, editable=False)
    place_taken         = models.ForeignKey(Place, blank=True, null=True, help_text="Add or select the place this photo was taken.", related_name="place_taken")
    places_in_photo     = models.ManyToManyField(Place, blank=True, null=True, help_text="Add or select locations visible in this photo.", related_name="places_in_photo")
    photographer        = models.ForeignKey(Person, blank=True, null=True, help_text="Add or select the photographer of this image.", related_name="photographer")
    organization        = models.ForeignKey(Organization, blank=True, null=True, help_text="Add or select the organization this image should be attributed to (i.e. Associated Press).", related_name="organization")
    copyright           = models.CharField(max_length=250, blank=True, null=True)
    people_in_photo     = models.ManyToManyField(Person, blank=True, null=True, help_text="Add or select people that appear in this photo.", related_name="people_in_photo")
    date_created        = models.DateTimeField(blank=True, null=True, help_text='If left blank, the system will attempt to populate it with photo EXIF data.')
    date_published      = models.DateTimeField(default=datetime.datetime.now, editable=False)
    file_size           = models.IntegerField(blank=True, null=True, help_text="Length of the photo file (in bytes)")
    make                = models.CharField(max_length=250, blank=True, null=True)
    model               = models.CharField(max_length=250, blank=True, null=True)
    date_raw            = models.CharField(max_length=250, blank=True, null=True)
    width               = models.CharField(max_length=250, blank=True, null=True)
    height              = models.CharField(max_length=250, blank=True, null=True)
    description         = models.TextField(blank=True, null=True)
    orientation         = models.CharField(max_length=250, blank=True, null=True)
    x_resolution        = models.CharField(max_length=250, blank=True, null=True)
    y_resolution        = models.CharField(max_length=250, blank=True, null=True)
    resolution_unit     = models.CharField(max_length=250, blank=True, null=True)
    software            = models.CharField(max_length=250, blank=True, null=True)
    host_computer       = models.CharField(max_length=250, blank=True, null=True)
    ycbcr_positioning   = models.CharField(max_length=250, blank=True, null=True)
    exposure            = models.CharField(max_length=250, blank=True, null=True)
    aperture            = models.CharField(max_length=250, blank=True, null=True)
    f_number            = models.CharField(max_length=250, blank=True, null=True)
    exposure_program    = models.CharField(max_length=250, blank=True, null=True)
    shutter_speed       = models.CharField(max_length=250, blank=True, null=True)
    exposure_bias       = models.CharField(max_length=250, blank=True, null=True)
    exposure_time       = models.CharField(max_length=250, blank=True, null=True)
    metering_mode       = models.CharField(max_length=250, blank=True, null=True)
    flash               = models.CharField(max_length=250, blank=True, null=True)
    focal_length        = models.CharField(max_length=250, blank=True, null=True)
    color_space         = models.CharField(max_length=250, blank=True, null=True)
    sensing_method      = models.CharField(max_length=250, blank=True, null=True)
    compression         = models.CharField(max_length=250, blank=True, null=True)
    gps_info            = models.CharField(max_length=250, blank=True, null=True)
    iso_speed_ratings   = models.CharField(max_length=250, blank=True, null=True)
    objects             = models.Manager()
    non_flickr_favorites= NonFlickrFavoriteManager()
    flickr_favorites    = FlickrFavoriteManager()
    flickr_photos       = FlickrPhotoManager()
    local_photos        = LocalPhotoManager()

    def __unicode__(self):
      return force_unicode(self.title);
    
    def is_horizontal(self):
      """ Returns True if this photo's height is less than it's width. """
      return self.image_height <= self.image_width
    
    def is_vertical(self):
      """ Returns True if this photo's height is greater than it's width. """
      return self.image_height >= self.image_width
    
    def flickr_photo(self):
      """ If this photo was imported from Flickr, returns the associated FlickrPhoto object. """
      try:
        return FlickrPhoto.objects.get(photo=self)
      except:
        return None
  
    def is_flickr_photo(self):
      """ Returns True if this photo was imported from Flickr. """
      if self.flickr_photo():
        return True
      else:
        return False
    
    def is_flickr_favorite(self):
      """ Returns True if this object is from Flickr and was uploaded by a person other than that specified in settings.FLICKR_USERID. """
      if self.flickr_photo():
        if self.flickr_photo().owner.nsid != settings.FLICKR_USERID:
          return True
      else:
        return False
      
    def source(self):
      """ Returns a string representation of the source for this photo (i.e. 'flickr', 'flickr favorite', or 'local'.) """
      source = 'local'
      if self.is_flickr_photo():
        source = "flickr"
      if self.is_flickr_favorite():
        source = "flickr favorite"
      return source
      
    def location(self):
      """ If this photo is geolocated, returns the associated GeolocatedItem object. """
      try:
        return GeolocatedItem.objects.get(content_type=ContentType.objects.get_for_model(Photo), object_id=self.id)
      except:
        return None
    
    def is_geolocated(self):
      """ Returns True if this item is geolocated. """
      if self.location():
        return True
      else:
        return False
      
    @permalink
    def get_absolute_url(self):
      """ Returns the URL to this photo's detail page. """
      y = self.date_published.strftime("%Y").lower()
      m = self.date_published.strftime("%b").lower()
      d = self.date_published.strftime("%d").lower()
      s = str(self.slug)
      if self.is_flickr_favorite():
        return ('photo_favorite_detail', None, {'year': y, 'month': m, 'day': d, 'slug': s})
      else:
        return ('photo_detail', None, {'year': y, 'month': m, 'day': d, 'slug': s})

    
    def _get_admin_thumbnail_url(self):
      """ Returns the URL appropriate for the admin interface's thumbnail image. """
      if self.flickr_photo():
        return self.flickr_photo.square_image_url
      else:
        try:
          return thumbnail(self.image.url, size=settings.ADMIN_THUMBNAIL_SIZE)
        except:
          return None
          
    def _admin_thumbnail(self):
      """Returns HTML for a thumbnail image, for displaying in the admin area."""
      from savoy.core.template_utils.templatetags.thumbnail import thumbnail
      return '<img src="%s" alt="%s" />' % (self._get_admin_thumbnail_url(),self.title)
      return self.image_url()
    
    _admin_thumbnail.short_description = 'Thumbnail'
    _admin_thumbnail.allow_tags = True
    
    def get_next_non_flickr_favorite_by_date_published(self):
      """ Returns the next photo which is not a Flickr Favorite by date published. """
      try:
        return self.get_next_by_date_published(flickrphoto__owner__nsid=settings.FLICKR_USERID)
      except:
        return None
        
    def get_previous_non_flickr_favorite_by_date_published(self):
      """ Returns the previous photo which is not a Flickr Favorite by date published. """
      try:
        return self.get_previous_by_date_published(flickrphoto__owner__nsid=settings.FLICKR_USERID)
      except:
        return None

    def get_next_flickr_favorite_by_date_published(self):
      """ Returns the next photo which is a Flickr Favorite by date published. """
      for photo in self.get_next_by_date_published():
        if photo.is_flickr_favorite():
          return photo
          break
      return

    def get_previous_flickr_favorite_by_date_published(self):
      """ Returns the previous photo which is a Flickr Favorite by date published. """
      for photo in self.get_previous_by_date_published():
        if photo.is_flickr_favorite():
          return photo
          break
      return
        
    def galleries(self):
      """ Returns a list of galleries this photo belongs to. """
      galleries = []
      for galleryphoto in self.galleryphoto_set.all():
        if galleryphoto.gallery not in galleries:
            galleries.append(galleryphoto.gallery)
      return galleries

    def _parse_and_add_exif(self):
      import EXIF
      tags                    = EXIF.process_file(open(self.image.path,'rb'))
      self.make               = smart_unicode(tags.get('Image Make', '')).strip()
      self.model              = smart_unicode(tags.get('Image Model', '')).strip()
      self.date_raw           = smart_unicode(tags.get('EXIF DateTimeOriginal', '')).strip()
      self.width              = smart_unicode(tags.get('EXIF ExifImageWidth', '')).strip()
      self.height             = smart_unicode(tags.get('EXIF ExifImageHeight', '')).strip()
      self.orientation        = smart_unicode(tags.get('Image Orientation', '')).strip()
      self.resolution_unit    = smart_unicode(tags.get('Image ResolutionUnit', '')).strip()
      self.x_resolution       = smart_unicode(tags.get('Image XResolution', '')).strip()
      self.y_resolution       = smart_unicode(tags.get('Image YResolution', '')).strip()
      self.software           = smart_unicode(tags.get('Image Software', '')).strip()
      self.exposure_time      = smart_unicode(tags.get('EXIF ExposureTime', '')).strip()
      self.exposure_bias      = smart_unicode(tags.get('EXIF ExposureBiasValue', '')).strip() 
      self.exposure_program   = smart_unicode(tags.get('EXIF ExposureProgram', '')).strip() 
      self.flash              = smart_unicode(tags.get('EXIF Flash', '')).strip() 
      self.f_number           = smart_unicode(tags.get('EXIF FNumber', '')).strip() 
      self.aperture           = smart_unicode(tags.get('EXIF MaxApertureValue', '')).strip() 
      self.metering_mode      = smart_unicode(tags.get('EXIF MeteringMode', '')).strip() 
      self.focal_length       = smart_unicode(tags.get('EXIF FocalLength', '')).strip() 
      self.color_space        = smart_unicode(tags.get('EXIF ColorSpace', '')).strip()
      self.focal_length       = smart_unicode(tags.get('EXIF FocalLength', '')).strip()
      self.ycbcr_positioning  = smart_unicode(tags.get('Image YCbCrPositioning', '')).strip()
      self.sensing_method     = smart_unicode(tags.get('EXIF SensingMethod', '')).strip()
      
      if not self.date_created:
          if self.date_raw:
              self.date_created = self.date_raw

    class Meta:
        ordering = ['-date_created']
        get_latest_by = 'date_created'

tagging.register(Photo, tag_descriptor_attr='_tags')

class FlickrPhoto(models.Model):
  """A FlickrPhoto object hangs on top of a Photo object to add Flickr-specific metadata."""
  photo               = models.ForeignKey(Photo)
  flickr_photo_id     = models.CharField(max_length=200)
  secret              = models.CharField(max_length=30)
  server              = models.PositiveSmallIntegerField()
  isfavorite          = models.BooleanField(blank=True, default=False)
  license             = models.IntegerField()
  rotation            = models.IntegerField()
  originalsecret      = models.CharField(max_length=30, blank=True)
  originalformat      = models.CharField(max_length=100)
  media               = models.CharField(max_length=200)
  owner               = models.ForeignKey('FlickrUser')
  ispublic            = models.BooleanField(default=True)
  isfriend            = models.BooleanField(default=False)
  isfamily            = models.BooleanField(default=False)
  permcomment         = models.BooleanField(blank=True)
  permaddmeta         = models.BooleanField(blank=True)
  cancomment          = models.BooleanField(default=False)
  canaddmeta          = models.BooleanField(default=False)
  comment_count       = models.PositiveIntegerField(max_length=5)
  date_posted         = models.DateTimeField()
  date_updated        = models.DateTimeField()
  date_taken_granularity = models.IntegerField()
  photo_page          = models.URLField(verify_exists=True)
  original_image_url  = models.URLField(blank=True, verify_exists=True)
  square_image_url    = models.URLField(blank=True, verify_exists=True)
  thumbnail_image_url = models.URLField(blank=True, verify_exists=True)
  small_image_url     = models.URLField(blank=True, verify_exists=True)
  medium_image_url    = models.URLField(blank=True, verify_exists=True)
  large_image_url     = models.URLField(blank=True, verify_exists=True)
 
  def __str__(self):
    return str(self.flickr_photo_id) + ": " + self.photo.title
    
  def is_video(self):
    """ Returns True if this Flickr 'photo' is a video. """
    return self.media == "video"

class FlickrUser(models.Model):
  """A FlickrUser is related to a FlickrPhoto and contains metadata about the person who owns the FlickrPhoto."""
  nsid                = models.CharField(max_length=200, primary_key=True)
  username            = models.CharField(max_length=200)
  realname            = models.CharField(blank=True, max_length=200)
  location            = models.CharField(blank=True, max_length=255)
  photos              = models.URLField(verify_exists=True)
  profile             = models.URLField(verify_exists=True)
  isadmin             = models.BooleanField(default=False)
  ispro               = models.BooleanField(default=False)
  iconserver          = models.IntegerField(blank=True, null=True)
  iconfarm            = models.IntegerField(blank=True, null=True)
  photocount          = models.IntegerField(blank=True, null=True)
  person              = models.ForeignKey(Person, blank=True, null=True)

  def __unicode__(self):
    return force_unicode(self.username + u" (" + self.realname + u")")

class FlickrNote(models.Model):
  """A FlickrNote is related to a FlickrPhoto and contains metadata about the photo's notes."""
  flickr_photo        = models.ForeignKey(FlickrPhoto)
  note_id             = models.CharField(max_length=200)
  author              = models.ForeignKey(FlickrUser)
  text                = models.TextField(blank=True)
  x                   = models.IntegerField()
  y                   = models.IntegerField()
  w                   = models.IntegerField()
  h                   = models.IntegerField()

  def __unicode__(self):
    return str(self.note_id)


class Video(models.Model):
    title               = models.CharField(max_length=250, help_text="Enter the title of this video.")
    slug                = models.SlugField(max_length=200, unique_for_date="date_created", help_text='The slug is a URL-friendly version of the title. It is auto-populated.')
    description         = models.TextField(blank=True, help_text='Add a caption for the video.')
    tags                = TagField(help_text="Add tags for this video.")
    video_file_url      = models.URLField(verify_exists=True, help_text="Enter the URL to the video file.")
    places_recorded     = models.ManyToManyField(Place, blank=True, null=True, help_text="Add or select locations this video was shot.", related_name="video_places_recorded")
    places_in_video     = models.ManyToManyField(Place, blank=True, null=True, help_text="Add or select locations that are visible in this video.", related_name="places_in_video")
    directors           = models.ManyToManyField(Person, blank=True, null=True, help_text="Add or select the directors of this video.", related_name="video_directors")
    producers           = models.ManyToManyField(Person, blank=True, null=True, help_text="Add or select the producers of this video.", related_name="video_producers")
    writers             = models.ManyToManyField(Person, blank=True, null=True, help_text="Add or select the writers of this video's script.", related_name="video_writers")
    videographers       = models.ManyToManyField(Person, blank=True, null=True, help_text="Add or select the photographers of this video.", related_name="video_videographers")
    organizations       = models.ManyToManyField(Organization, blank=True, null=True, help_text="Add or select the organizations this video should be attributed to (i.e. Associated Press).", related_name="video_organizations")
    people_in_video     = models.ManyToManyField(Person, blank=True, null=True, help_text="Add or select people that appear in this video.", related_name="people_in_video")
    date_created        = models.DateTimeField(default=datetime.datetime.now, blank=True, null=True, help_text="Enter the date the video was created.")
    date_uploaded       = models.DateTimeField(default=datetime.datetime.now, editable=False)
    file_size           = models.IntegerField(blank=True, null=True, help_text="Length of the video file (in bytes)")
    video_type          = models.IntegerField(default=1, choices=VIDEO_TYPE_CHOICES)
    width               = models.IntegerField('Video width', default=640, help_text='Width of video in pixels.')
    height              = models.IntegerField('Video height', default=480, help_text='Height of video in pixels.')
    thumbnail_photo     = models.ImageField(upload_to='video/thumbnails/%Y/%m/%d', width_field='thumbnail_width', height_field='thumbnail_height', help_text="Upload a thumbnail photo to be used with this audio clip.", blank=True, null=True)
    thumbnail_width     = models.IntegerField('thumbnail width', blank=True, null=True)
    thumbnail_height    = models.IntegerField('thumbnail height', blank=True, null=True)
        
    def __unicode__(self):
        return force_unicode(self.title)

    def get_mime_type(self):
        """Return the correct mime-type for a video depending on its video_type"""
        if self.video_type == 1:
            return "video/quicktime"
        elif self.video_type == 2:
            return "video/mp4"
        elif self.video_type == 3:
            return "video/mp4"
        elif self.video_type == 4:
            return "video/3gpp"
        elif self.video_type == 5:
            return "application/x-shockwave-flash"

    class Meta:
        ordering = ('-date_created',)


class Audio(models.Model):
    title               = models.CharField(max_length=250, help_text="Enter the title of this audio clip.")
    slug                = models.SlugField(max_length=200, unique_for_date="date_created", help_text='The slug is a URL-friendly version of the title. It is auto-populated.')
    description         = models.TextField(blank=True, help_text='Add a caption for the audio clip.')
    tags                = TagField(help_text="Add tags for this audio clip.")
    audio_file_url      = models.URLField(verify_exists=True, help_text="Enter the URL to the audio file.")
    places_recorded     = models.ManyToManyField(Place, blank=True, help_text="Add or select locations where this audio was recorded.", related_name="places_recorded")
    directors           = models.ManyToManyField(Person, blank=True, null=True, help_text="Add or select the directors of this audio clip.", related_name="audio_directors")
    producers           = models.ManyToManyField(Person, blank=True, null=True, help_text="Add or select the producers of this audio clip.", related_name="audio_producers")
    writers             = models.ManyToManyField(Person, blank=True, null=True, help_text="Add or select the writers of this audio clip's script.", related_name="audio_writers")
    audio_engineers     = models.ManyToManyField(Person, blank=True, null=True, help_text="Add or select the audio engineers for this audio clip.", related_name="audio_engineers")
    organizations       = models.ManyToManyField(Organization, blank=True, null=True, help_text="Add or select the organizations this audio should be attributed to (i.e. Associated Press).", related_name="audio_organizations")
    people_in_audio     = models.ManyToManyField(Person, blank=True, null=True, help_text="Add or select people that are heard in this audio clip.", related_name="people_in_audio")
    date_created        = models.DateTimeField(default=datetime.datetime.now, blank=True, null=True, help_text="Enter the date the audio clip was created.")
    date_uploaded       = models.DateTimeField(default=datetime.datetime.now, editable=False)
    file_size           = models.IntegerField(blank=True, null=True, help_text="Length of the audio file (in bytes)")
    audio_type          = models.IntegerField(default=1, choices=AUDIO_TYPE_CHOICES)
    thumbnail_photo     = models.ImageField(upload_to='audio/thumbnails/%Y/%m/%d', width_field='thumbnail_width', height_field='thumbnail_height', help_text="Upload a thumbnail photo to be used with this audio clip.", blank=True, null=True)
    thumbnail_width     = models.IntegerField('thumbnail width', blank=True, null=True)
    thumbnail_height    = models.IntegerField('thumbnail height', blank=True, null=True)

    def __unicode__(self):
        return force_unicode(self.title)

    class Meta:
        ordering = ('-date_created',)
        verbose_name_plural = "Audio files"

class Document(models.Model):
    title               = models.CharField(max_length=250, help_text="Enter the title of this document.")
    slug                = models.SlugField(max_length=200, unique_for_date="date_created", help_text='The slug is a URL-friendly version of the title. It is auto-populated.')
    description         = models.TextField(blank=True, help_text='Add a caption for the document.')
    tags                = TagField(help_text="Add tags for this document.")
    document            = models.FileField(upload_to='doc/%Y/%m/%d/', help_text="Upload the document file.")
    creators            = models.ManyToManyField(Person, blank=True, null=True, help_text="Add or select the creators of this document.", related_name="doc_creators")
    organizations       = models.ManyToManyField(Organization, blank=True, null=True, help_text="Add or select the organizations this audio should be attributed to (i.e. Associated Press).", related_name="doc_organizations")
    people_in_doc       = models.ManyToManyField(Person, blank=True, null=True, help_text="Add or select people that are referred to in this document.", related_name="people_in_doc")
    date_created        = models.DateTimeField(default=datetime.datetime.now, blank=True, null=True, help_text="Enter the date the document was created.")
    date_uploaded       = models.DateTimeField(default=datetime.datetime.now, editable=False)
    file_size           = models.IntegerField(blank=True, null=True, help_text="Length of the audio file (in bytes)")
    file_type          = models.IntegerField(default=1, choices=DOC_TYPE_CHOICES)
    thumbnail_photo     = models.ImageField(upload_to='doc/thumbnails/%Y/%m/%d', width_field='thumbnail_width', height_field='thumbnail_height', help_text="Upload a thumbnail photo to be used with this document.", blank=True, null=True)
    thumbnail_width     = models.IntegerField('thumbnail width', blank=True, null=True)
    thumbnail_height    = models.IntegerField('thumbnail height', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-date_created',)


class EmbeddedMediaType(models.Model):
  name = models.CharField(max_length=200, help_text="Enter the name of the media type, such as 'video,' or 'audio'.")
  slug = models.SlugField(help_text="The slug is a URL-friendly version of the name. It is auto-populated.")

  def __unicode__(self):
    return force_unicode(self.name)


class EmbeddedMedia(models.Model):
  """An EmbeddedMedia object is any media that uses a chuck of HTML as embed code, such as a video from YouTube or similar."""
  title               = models.CharField(max_length=250, help_text="Enter the title of this embedded media object.")
  slug                = models.SlugField(help_text="The slug is a URL-friendly version of the title. It is auto-populated.")
  description         = models.TextField(blank=True, help_text="Enter a description for this embedded media object.")
  tags                = TagField(help_text="Add tags for this embedded media object.")
  type                = models.ForeignKey(EmbeddedMediaType, help_text="Select the embedded media type for this object.")
  embed_code          = models.TextField(help_text="Enter the embedding code for this object.")
  date_created        = models.DateTimeField(default=datetime.datetime.now, editable=False)
  date_published      = models.DateTimeField(default=datetime.datetime.now)

  def __unicode__(self):
    return force_unicode(self.title)

  @permalink
  def get_absolute_url(self):
    """ Returns the URL to this embedded media object's detail page. """
    y = self.date_published.strftime("%Y").lower()
    m = self.date_published.strftime("%b").lower()
    d = self.date_published.strftime("%d").lower()
    s = str(self.slug)
    return ('embedded_media_detail', None, {'year': y, 'month': m, 'day': d, 'slug': s})

  class Meta:
    verbose_name_plural = "Embedded media objects"

signals.post_delete.connect(GeolocatedItem.objects.remove_orphans, sender=Photo)