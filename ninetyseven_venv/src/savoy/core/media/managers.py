from django.db import models

class LocalPhotoManager(models.Manager):
  """
  Custom manager for photos which only returns status which are local (i.e. not from flickr).
  """
  def get_query_set(self):
    return super(LocalPhotoManager, self).get_query_set().filter(flickrphoto__isnull=True)

class FlickrPhotoManager(models.Manager):
  """
  Custom manager for photos which only returns status which are from flickr.
  """
  def get_query_set(self):
    return super(FlickrPhotoManager, self).get_query_set().exclude(flickrphoto__isnull=True)


class FlickrFavoriteManager(models.Manager):
  """
  Custom manager for photos which only returns status which are flickr favorite.
  """
  def get_query_set(self):
    return super(FlickrFavoriteManager, self).get_query_set().exclude(flickrphoto__isnull=True).exclude(flickrphoto__owner__nsid=settings.FLICKR_USERID)


class NonFlickrFavoriteManager(models.Manager):
  """
  Custom manager for photos which only returns photos which are from flickr, but not flickr favorites.
  """
  def get_query_set(self):
    return super(NonFlickrFavoriteManager, self).get_query_set().exclude(flickrphoto__isnull=True).filter(flickrphoto__owner__nsid=settings.FLICKR_USERID)