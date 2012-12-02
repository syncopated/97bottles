import datetime

from django.db import models
from django.db.models import permalink
from django.db.models import permalink
from tagging.fields import TagField

from savoy.core.people.models import Person
from savoy.core.media.models import Video, Audio
from savoy.core.constants import PODCAST_SHOW_STATUS_CHOICES, PODCAST_EPISODE_STATUS_CHOICES


class Show(models.Model):
  name            = models.CharField(max_length=200, help_text="Enter the name of the show.")
  slug            = models.SlugField(help_text="The slug is a URL-friendly version of the name. It is auto-populated.")
  hosts           = models.ManyToManyField(Person)
  date_created    = models.DateTimeField(default=datetime.datetime.now)
  status          = models.IntegerField('Show status', choices=PODCAST_SHOW_STATUS_CHOICES, default=1)
  featured        = models.BooleanField('Featured', default=False)
  tags            = TagField(help_text="Add tags for this show (space separated).")

  def __unicode__(self):
    return self.name

  def get_absolute_url(self):
    """ Returns the URL for this show's detail page. """
    return ('savoy.contrib.podcasts.views.show_detail', (), { 'slug': self.slug })

  def get_podcast_url(self):
    """ Returns the URL for the RSS (podcast) feed for this show. """
    from django.core import urlresolvers
    kwargs = { 'url': 'episodes-for-show','feed_dict': { 'episodes-for-show': LatestEpisodesPerShow } }
    return urlresolvers.reverse("podcast_feeds", kwargs=kwargs)



class Episode(models.Model):
  show            = models.ForeignKey(Show, help_text="Select the show this episode belongs to.")
  title           = models.CharField(max_length=200, help_text="Enter the title of this episode.")
  slug            = models.SlugField(help_text="The slug is a URL-friendly version of the title. It is auto-populated.")
  description     = models.TextField(blank=True, help_text="Enter a brief description of this episode.")
  summary         = models.TextField(blank=True, help_text='Enter a brief summary of this blog entry.', db_index=True,)
  date_published  = models.DateTimeField(help_text="Select the date and time this episode should be published.", default=datetime.datetime.now)
  date_created    = models.DateTimeField(editable=False, default=datetime.datetime.now)
  date_updated    = models.DateTimeField(editable=False)
  tags            = TagField(help_text="Add tags for this entry (space separated).")
  status          = models.IntegerField('Entry status', help_text="Select the status of this episode.", choices=PODCAST_EPISODE_STATUS_CHOICES, default=2)
  featured        = models.BooleanField('Featured', default=False, help_text="Select 'True' if if this is currently a featured episode.")

  def __unicode__(self):
    return self.title

  @permalink
  def get_absolute_url(self):
    """ Returns the URL of the detail page for this Episode. """
    try:
      y = self.date_published.strftime("%Y").lower()
      m = self.date_published.strftime("%b").lower()
      d = self.date_published.strftime("%d").lower()
      s = str(self.slug)
      return ('savoy.contrib.podcasts.views.episode_detail', (), { 'show_slug': str(self.show.slug), 'year': y, 'month': m, 'day': d, 'slug': s })
    except:
      return None
  
  def episode_number(self):
    """ Returns the sequential number for this episode, based on date published. """
    i = 1
    for episode in self.show.episode_set.all().order_by('date_published'):
      if episode == self:
        return i
      else:
        i = i + 1

  def save(self, force_insert=False, force_update=False):
    """ Sets the update date, and then saves the Episode. """
    self.date_updated = datetime.datetime.now()
    super(Episode, self).save(force_insert=force_insert, force_update=force_update) # Call the "real" save() method


class PodcastVideo(models.Model):
  episode         = models.ForeignKey(Episode, help_text="Select the episode this video file is for.", related_name="video_files")
  video           = models.ForeignKey(Video, help_text="Select the video file for this episode.", related_name="podcast_episodes")
  
  class Meta:
    verbose_name_plural = "Video for episode"

  def __unicode__(self):
    return self.video.title


class PodcastAudio(models.Model):
  episode         = models.ForeignKey(Episode, help_text="Select the episode this audio file is for.", related_name="audio_files")
  audio           = models.ForeignKey(Audio, help_text="Select the audio file for this episode.", related_name="podcast_episodes")

  class Meta:
    verbose_name_plural = "Audio for episode"

  def __unicode__(self):
    return self.audio.title
