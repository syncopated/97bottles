from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from ninetyseven.apps.relationships.managers import *

class Relationship(models.Model):
    """ Relationship model """
    from_user       = models.ForeignKey(User, related_name='relationships')
    to_user         = models.ForeignKey(User, related_name='relationships_to')
    created         = models.DateTimeField(auto_now_add=True)
    objects         = RelationshipManager()
    
    class Meta:
        unique_together = (('from_user', 'to_user'),)
        verbose_name = _('relationship')
        verbose_name_plural = _('relationships')
        db_table = 'relationships'

    def __unicode__(self):
        return u'%s is connected to %s.' % (self.from_user, self.to_user)
    
    def get_reciprocal_relationship(self):
      """
      Checks for a matching reciprocal relationship. If one exists, returns it. If not, returns None.
      """
      try:
        return Relationship.objects.get(to_user=self.from_user, from_user=self.to_user)
      except:
        return None
    
    def is_reciprocal(self):
      """
      Returns True if there exists a matching reciprocal relationship.
      """
      if self.get_reciprocal_relationship():
        return True
      else:
        return False