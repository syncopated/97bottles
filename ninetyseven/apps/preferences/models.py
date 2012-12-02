from django.db import models
from django.db.models import signals, permalink
from django.contrib.auth.models import User

from ninetyseven.apps.preferences.managers import UserPreferenceManager

class UserPreference(models.Model):
  user                = models.OneToOneField(User, primary_key=True, related_name="preferences")
  email_notification  = models.BooleanField(default=True, help_text="Check this box if you wish to receive e-mail notifications from 97 Bottles.")
  objects             = UserPreferenceManager()
  
  def __unicode__(self):
    return self.user.username
    
# When a user is saved, create or update a user info object.
signals.post_save.connect(UserPreference.objects.create_or_update, sender=User)
