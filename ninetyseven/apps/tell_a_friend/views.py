from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

from ninetyseven.apps.tell_a_friend.forms import *

@login_required
def tell_a_friend(request, success_template_name='tell_a_friend/form_success.html', email_body_template='tell_a_friend/email_body.txt', email_subject_template='tell_a_friend/email_subject.txt', mimetype='text/html'):
  if request.method == 'POST':
    form = TellAFriendForm(request.POST)
    if form.is_valid():
      site = Site.objects.get(pk=settings.SITE_ID)
      recipient = form.cleaned_data['recipient']
      context = { 'user': request.user, 'recipient': recipient }
      subject = render_to_string(email_subject_template, context)
      message = render_to_string(email_body_template, context)
      email = EmailMessage(subject, message, settings.REPLY_EMAIL, ['%s' % recipient])
      email.send(fail_silently=False)
      return render_to_response("tell_a_friend/form_success.html", context, context_instance=RequestContext(request))
    else:
      context = { 'form': form }
      return render_to_response("tell_a_friend/form.html", context, context_instance=RequestContext(request))
  else:
    form = TellAFriendForm()
    context = { 'form': form }
    return render_to_response("tell_a_friend/form.html", context, context_instance=RequestContext(request))
    