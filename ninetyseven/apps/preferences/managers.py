from django.db import models
from django.contrib.contenttypes.models import ContentType

from ninetyseven.apps.preferences.models import *

class UserPreferenceManager(models.Manager):
  def create_or_update(self, instance, **kwargs):
    """
    Create or update a UserPreferences from some User.
    """
    user_preference, created = self.get_or_create(
      user = instance,
    )
    return user_preference