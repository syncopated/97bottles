import datetime
import md5

from django.db import models
from django.conf import settings
from django.db.models import permalink
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User

from savoy.core.people.models import Person
from savoy.core.media.models import FlickrUser
from savoy.contrib.comments.managers import *

class NameBlacklistItem(models.Model):
  """
  The name blacklist is a list of author names to reject comments from.
  """
  name = models.CharField(max_length=250)
  reason = models.TextField(blank=True)

  def __unicode__(self):
    return self.name


class EmailBlacklistItem(models.Model):
  """
  The email blacklist is a list of author email addresses to reject comments from.
  """
  email_address = models.EmailField()
  reason = models.TextField(blank=True)

  def __unicode__(self):
    return self.email_address


class IPBlacklistItem(models.Model):
  """
  The name blacklist is a list of author names to reject comments from.
  """
  ip_address = models.IPAddressField()
  reason = models.TextField(blank=True)

  def __unicode__(self):
    return self.ip_address


class URLBlacklistItem(models.Model):
  """
  The name blacklist is a list of author names to reject comments from.
  """
  url = models.URLField()
  reason = models.TextField(blank=True)

  def __unicode__(self):
    return self.url


class EmailWhitelistItem(models.Model):
  """
  The email whitelist is a list of author email addresses to blindly accept comments from.
  """
  email_address = models.EmailField()
  reason = models.TextField(blank=True)

  def __unicode__(self):
    return self.email_address


class Comment(models.Model):
  content_type                    = models.ForeignKey(ContentType)
  object_id                       = models.IntegerField()
  content_object                  = generic.GenericForeignKey()
  person                          = models.ForeignKey(Person, blank=True, null=True)
  author_name                     = models.CharField(max_length=150)
  author_email_address            = models.EmailField(max_length=250)
  author_email_address_hash       = models.CharField(max_length=250, blank=True, null=True)
  author_url                      = models.URLField(blank=True, null=True)
  author_ip_address               = models.IPAddressField()
  author_user_agent_string        = models.CharField(max_length=250, blank=True)
  title                           = models.CharField(blank=True, max_length=250)
  body                            = models.TextField()
  featured                        = models.BooleanField(default=False)
  trollish                        = models.BooleanField(default=False)
  approved                        = models.BooleanField(default=False)
  whitelisted                     = models.BooleanField(default=False)
  blacklisted                     = models.BooleanField(default=False)
  failed_akismet                  = models.BooleanField(default=False)
  completed_spam_check            = models.BooleanField(default=False)
  date_submitted                  = models.DateTimeField(default=datetime.datetime.now)
  objects                         = models.Manager()
  approved_comments               = ApprovedCommentManager()
  orphaned_comments               = OrphanedCommentManager()
  featured_comments               = FeaturedCommentManager()
  exclude_flickr_favorites        = NonFlickrFavoriteApprovedCommentManager()
    
  def __unicode__(self):
      return "%s: %s..." % (self.author_name, self.body[:50])
      
  def is_flickr_comment(self):
    """ Returns True if this comment was imported from Flickr. """
    if FlickrComment.objects.get(comment=self):
      return True
    else:
      return False

  def source(self):
    """ Returns a string representation of the source for this comment (i.e. 'flickr' or 'local'). """
    if self.is_flickr_comment():
      return "flickr"
    else:
      return "local"

  @permalink
  def get_absolute_url(self):
    """
    Returns the absolute URL to the comment: the URL of the object it's attached to, plus and anchor.
    """
    try:
      return '%s#c%s' % (self.parent_object().get_absolute_url(), self.id)
    except AttributeError:
        return ""
  
  def parent_object(self):
    """
    Returns the object that this is a comment on. If that item is another comment
    (in the case of threaded comments), keeps going up the chain until it find a 
    parent object that is another ContentType.
    """
    from django.core.exceptions import ObjectDoesNotExist
    try:
      if self.content_type == ContentType.objects.get_for_model(Comment):
        return self.content_object.parent_object()
      else:
        return self.content_type.get_object_for_this_type(pk=self.object_id)
    except ObjectDoesNotExist:
      return None

  def _akismet_spam_check(self):
    """
    Checks the comment against the Akismet spam prevention web service. Returns "spam" if the
    comment is found to be spam, "ham" if the comment isn't found to be spam, and "error" if
    the check doesn't complete successfully.
    """
    from akismet import Akismet, AkismetError
    import unicodedata
    akismet = Akismet(key=settings.AKISMET_API_KEY, blog_url=settings.AKISMET_SITE_URL, agent=settings.AKISMET_USER_AGENT)
    comment_data = {
      'user_ip': self.author_ip_address,
      'user_agent': self.author_user_agent_string,
      'comment_author': unicodedata.normalize('NFKD', self.author_name).encode('ascii','ignore'),
      'comment_author_email': self.author_email_address,
      'comment_author_url': self.author_url,
    }
    try:
      # Pass the comment through Akisment and find out if it thinks it's spam.
      is_spam = akismet.comment_check(comment=unicodedata.normalize('NFKD', unicode(self.body)).encode('ascii','ignore'), data=comment_data)
      if is_spam == True:
        return "spam"
      elif is_spam == False:
        return "ham"
    except AkismetError:
      pass
      return "error"
  
  def _is_whitelisted(self):
    """
    Returns True is the comment matches our whitelist.
    """
    try:
      item = EmailWhitelistItem.objects.get(email_address=self.author_email_address)
      return True
    except:
      return False
  
  def _is_blacklisted(self):
    """
    Returns True is the comment matches one of our blacklists.
    """
    blacklisted = False
    if NameBlacklistItem.objects.all().count() != 0:
      for item in NameBlacklistItem.objects.all():
        if item.name in self.author_name:
          return True
    if EmailBlacklistItem.objects.all().count() != 0:
      for item in EmailBlacklistItem.objects.all():
        if item.email_address in self.author_email_address:
          return True
    if URLBlacklistItem.objects.all().count() != 0:
      for item in URLBlacklistItem.objects.all():
        if item.url in self.author_url:
          return True
    if IPBlacklistItem.objects.all().count() != 0:
      for item in IPBlacklistItem.objects.all():
        if item.ip_address in self.author_ip_address:
          return True
    return blacklisted
  
  def _spam_check(self):
    """
    Checks the comment for spam and other undesirables.
    """
    # Set all the possible flags to False upfront.
    delete_me = is_spam = whitelisted = blacklisted = akismet_error = approved = False
  
    # Next, see if Akismet will sign off on the comment.
    akismet_result = self._akismet_spam_check()
    if akismet_result == "spam":
      # If Akismet reports the comment is spam, mark it for deletion.
      is_spam = True
      delete_me = True
    elif akismet_result == "ham":
      #  If it's ham, approve it.
      approved = True
    elif akismet_result == "error":
      # If there was some error in the Akismet-checking process, unapprove the comment
      # and flag it for notification later.
      akismet_error = True
    
    # If we fail local spam checks, unapprove and delete the comment.
    if self._is_blacklisted() == True:
      approved = False
      delete_me = True
      blacklisted = True
      
    # If the e-mail is in our whitelist, approve and save the message, even despite any other
    # checks which may have raised flags.
    if self._is_whitelisted():
      approved = True
      whitelisted = True
      blacklisted = False
      delete_me = False
      is_spam = False
    
    results = {
        'delete': delete_me,
        'blacklisted': blacklisted,
        'whitelisted': whitelisted,
        'approved': approved,
        'akismet_spam': is_spam,
        'akismet_error': akismet_error,
      }
    
    return results
  
  def save(self, force_insert=False, force_update=False):
    # Figure out which content item (blog post, link, etc.) we're dealing with.
    content_object = self.content_object
    
    if self.completed_spam_check:
      # If passed_spam_check is Ture, then this is an old comment and we're probably editing in the admin.
      # Therefore, changes are authoritative, and we don't need to go through all the comment spam measures.
      super(Comment, self).save()
    else:
      # If passed_spam_check is False, we need to run akismet and test aganist our blacklists.
      # We only do this once.
      spam_check = self._spam_check()
      self.completed_spam_check = True
      
      # If the message isn't marked for deletion, save the comment
      if not spam_check['delete']:
        self.approved = spam_check['approved']
        self.whitelisted = spam_check['whitelisted']
        self.blacklisted = spam_check['blacklisted']
        self.passed_akismet = spam_check['akismet_spam']
        self.author_email_address_hash = md5.new(self.author_email_address).hexdigest()
        super(Comment, self).save(force_insert=force_insert, force_update=force_update)
      else:
        # If the message is marked for deletion, don't save it.
        return
        
  class Meta:
    ordering                      = ('-date_submitted',)
    get_latest_by                 = 'date_submitted'


class FlickrComment(models.Model):
  """A FlickrComment keeps comments left on Flickr. It hangs off the Comment model, storing Flickr-specific metadata."""
  comment             = models.ForeignKey(Comment)
  flickr_comment_id   = models.CharField(blank=True, max_length=200)
  author              = models.ForeignKey(FlickrUser)
  url                 = models.URLField(blank=True, verify_exists=True)

  def __str__(self):
    return "FlickrComment"
