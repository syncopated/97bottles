from django.db import models
from django.contrib.auth.models import User

from ninetyseven.apps.invites.managers import InviteManager

class Invite(models.Model):
  """
  An invite is an invitation to use this site.
  """
  user            = models.ForeignKey(User, related_name="invites")
  email           = models.EmailField(blank=True, help_text="E-mail address of the person being invited.")
  activation_key  = models.CharField(max_length=40, blank=True)
  redeemed        = models.BooleanField(default=False)

  objects   = InviteManager()
  
  def __unicode__(self):
    return "%s: %s" % (self.user, self.email)
  
  def save(self, force_insert=False, force_update=False):
    if self.email and not self.activation_key:
      Invite.objects.send_invite(self)
    super(Invite, self).save(force_insert=force_insert, force_update=force_update)
