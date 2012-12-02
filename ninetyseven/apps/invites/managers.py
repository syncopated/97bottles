from django.db import models
from django.conf import settings

class InviteManager(models.Manager):
  def add_for_user(self, instance, num=1, **kwargs):
    """
    Grants a user (instance) a number (num) of invites.
    """
    from ninetyseven.apps.invites.models import Invite
    while num > 0:
      Invite.objects.create(user=instance)
      num = num -1
      
  def send_invite(self, instance, email_subject_template="invites/invite_email_subject.html", email_body_template="invites/invite_email_body.html", **kwargs):
    """
    Given an invite, creates an activation key and sends the invitation e-mail.
    """
    invite = instance
    if invite.email:
      import sha
      import random
      from django.core.mail import EmailMessage
      from django.contrib.sites.models import *
      from django.template.loader import render_to_string
      salt = sha.new(str(random.random())).hexdigest()[:5]
      invite.activation_key = sha.new(salt+invite.email).hexdigest()
      invite.save()
      site = Site.objects.get(pk=settings.SITE_ID)
      context = { 'invite': invite, 'site': site }
      subject = render_to_string(email_subject_template, context)
      message = render_to_string(email_body_template, context)
      email = EmailMessage(subject, message, settings.REPLY_EMAIL, ['%s' % invite.email])
      email.send(fail_silently=False)