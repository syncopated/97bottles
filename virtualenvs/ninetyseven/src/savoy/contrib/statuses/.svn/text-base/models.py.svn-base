import datetime

from django.db import models
from django.conf import settings
from django.db.models import permalink

from savoy.core.people.models import Person

class ReplyStatusManager(models.Manager):
  """
  Custom manager for comments which only returns status which are replies (based on @username syntax).
  """
  def get_query_set(self):
    return super(NonReplyStatusManager, self).get_query_set().filter(body__startswith="@")


class NonReplyStatusManager(models.Manager):
  """
  Custom manager for comments which only returns status which are not replies (based on @username syntax).
  """
  def get_query_set(self):
    return super(NonReplyStatusManager, self).get_query_set().exclude(body__startswith="@")


class Status(models.Model):
  """
  A Status is a brief update on what someone's doing, a la Twitter.
  """
  body                      = models.TextField()
  date_published            = models.DateTimeField(default=datetime.datetime.now)
  person                    = models.ForeignKey(Person, blank=True, null=True)
  objects                   = models.Manager()
  non_reply_statuses        = NonReplyStatusManager()
  reply_statuses            = ReplyStatusManager()

  class Meta:
    verbose_name_plural     = "Statuses"
    ordering                = ['-date_published']

  def __unicode__(self):
    return self.body
  
  
  @permalink
  def get_absolute_url(self):
    y = self.date_published.strftime("%Y").lower()
    m = self.date_published.strftime("%b").lower()
    d = self.date_published.strftime("%d").lower()
    i = str(self.id)
    return ('status_detail', (), {'year': y, 'month': m, 'day': d, 'object_id': i})
    
  def twitter_status(self):
    """ If this status was imported from Twitter, returns the associated TwitterStatus object. """
    try:
      return TwitterStatus.objects.get(status=self)
    except:
      return None
  
  def is_twitter_status(self):
    """ Returns True if this status was imported from Twitter. """
    if self.twitter_status():
      return True
    else:
      return False
    
  def is_friends_status(self):
    """ Returns True if this status is from Twitter and was created by someone other than the person specified in settings.TWITTER_USERNAME. """
    if self.twitter_status():
      if self.twitter_status.twitter_user.user_name != settings.TWITTER_USERNAME:
        return True
    else:
      return False
  
  def is_reply(self):
    """ Returns True if this status is a reply (starts with '@'). """
    if self.body.startswith('@'):
      return True
    else:
      return False
  
  def in_reply_to(self):
    """ If this status is a reply, returns the username of the user who is being replied to. """
    if self.is_reply():
      words = self.body.split(" ")
      if words[0].endswith(":"):
        length = len(words[0])
        return words[0][1:length-1]
      else:
        return words[0][1:]
    else:
      return None
      
  
  def body_strip_reply(self):
    """ Returns the body of the status. If it starts with '@username', that bit is stripped. """
    if self.is_reply():
      words = self.body.split(" ")
      return " ".join(words[1:])
    else:
      return self.body
  
  def in_reply_to_url(self):
    """ If this status is a reply, returns the twitter URL of the person being replied to. """
    if self.is_reply():
      return "http://twitter.com/%s/" % self.in_reply_to
    else:
      return None
      
  def twitter_user(self):
    """ If this status is from Twitter, returns the associated TwitterUser object. """
    if self.is_twitter_status():
      return self.twitter_status.twitter_user
    else:
      return None

class TwitterUser(models.Model):
  """Status submitted to twitter"""
  user_id           = models.IntegerField(max_length=250)
  user_name         = models.CharField(max_length=250)
  screen_name       = models.CharField(max_length=250)
  location          = models.CharField(max_length=250, blank=True)
  description       = models.TextField(blank=True)
  profile_image_url = models.URLField(blank=True, verify_exists=True)
  url               = models.URLField(blank=True, verify_exists=True)

  def __unicode__(self):
    return self.user_name + " (" + self.screen_name + ")"

class TwitterStatus(models.Model):
  """Status submitted to twitter"""
  status                    = models.ForeignKey(Status)
  twitter_user              = models.ForeignKey(TwitterUser)
  twitter_status_id         = models.CharField(max_length=250)

  def __unicode__(self):
    return "%s: %s" % (self.twitter_user.user_name, self.status.date_published)