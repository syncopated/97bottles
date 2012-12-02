from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

class FeaturedCommentManager(models.Manager):
  """
  Custom manager for comments which only returns comments marked as "featured".
  """
  def get_query_set(self):
      return super(FeaturedCommentManager, self).get_query_set().filter(approved=True, is_featured=True)

class ApprovedCommentManager(models.Manager):
  """
  Custom manager for comments which only returns comments marked as "approved".
  """
  def get_query_set(self):
      return super(ApprovedCommentManager, self).get_query_set().filter(approved=True)

class OrphanedCommentManager(models.Manager):
  """
  Custom manager for comments which only returns comments whose content object is None.
  """
  def get_query_set(self):
      from savoy.contrib.comments.models import Comment
      orphaned_comments = []
      for comment in Comment.objects.all():
          if comment.content_object == None:
              orphaned_comments.append(comment.id)
      return super(OrphanedCommentManager, self).get_query_set().filter(id__in=orphaned_comments)

class NonFlickrFavoriteApprovedCommentManager(models.Manager):
  """
  Custom manager for comments which only returns comments marked as "approved" and excludes comments on flickr favorites.
  """
  def get_query_set(self):
      from savoy.core.media.models import Photo
      photo_favorite_queryset = Photo.objects.exclude(flickrphoto__owner__nsid=settings.FLICKR_USERID).values('id')
      photo_favorite_ids = [ p['id'] for p in photo_favorite_queryset ]
      photo_content_type = ContentType.objects.get_for_model(Photo)
      return super(NonFlickrFavoriteApprovedCommentManager, self).get_query_set().filter(approved=True).exclude(content_type=photo_content_type, object_id__in=photo_favorite_ids)