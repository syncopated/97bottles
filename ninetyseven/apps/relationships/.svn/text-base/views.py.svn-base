from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import models
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.sites.models import Site

Relationship = models.get_model('relationships', 'relationship')
Profile = models.get_model('profiles', 'profile')

@login_required
def follow_unfollow(request, to_user_id, success_template_name='relationships/follow_unfollow_success.html', email_body_template='relationships/follow_email_body.txt', email_subject_template='relationships/follow_email_subject.txt', mimetype='text/html'):
  """ Toggles between following and unfollowing. """
  to_user = get_object_or_404(User, pk=to_user_id)
  from_user = request.user
  relationship, created = Relationship.objects.get_or_create(from_user=from_user, to_user=to_user)
  if created:
    if to_user.preferences.email_notification:
      site = Site.objects.get(pk=settings.SITE_ID)
      context = {
        'relationship': relationship,
        'site': site
      }
      subject = render_to_string(email_subject_template, context)
      message = render_to_string(email_body_template, context)
      if to_user.email:
        email = EmailMessage(subject, message, settings.REPLY_EMAIL, ['%s' % to_user.email])
        email.send(fail_silently=False)
  else:
    relationship.delete()
    relationship = None
  if request.is_ajax():
    context = "{'success': 'true', 'to_user_id': '%s'}" % (to_user.id)
    return HttpResponse(context, mimetype="application/json")
  else:
    template_name = success_template_name
    context = {'to_user': to_user, 'relationship': relationship }
    return render_to_response(template_name, context, context_instance=RequestContext(request), mimetype=mimetype)

def user_relationships(request, username, template_name='relationships/user_relationships.html'):
  """
  Displays all the relationships for the given user.
  """
  user = get_object_or_404(User, username=username)
  profile = Profile.objects.get(user=user)
  relationships = Relationship.objects.relationships_for_user(user)
  return render_to_response(template_name, RequestContext(request, { 'profile': profile, 'user': user, 'friends': relationships['friends'], 'following': relationships['following'], 'followers': relationships['followers'] }))
    