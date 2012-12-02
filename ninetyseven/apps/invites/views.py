from django.shortcuts import render_to_response
from django.template import RequestContext

from ninetyseven.apps.invites.models import *
from ninetyseven.apps.invites.forms import *

def send_invite(request):
  try:
    invite = Invite.objects.filter(user=request.user, email="", activation_key="")[0]
  except:
    context = { }
    return render_to_response("invites/no_invites_to_send.html", context, context_instance=RequestContext(request))
  if request.method == "POST":
    form = InviteForm(request.POST, instance=invite, prefix="invite")
    if form.is_valid():
      invite = form.save(commit=False)
      invite.save()
      context = { 'invite': invite, }
      return render_to_response('invites/invite_sent.html', context, context_instance=RequestContext(request))
    else:
      context = { 'invite_form': form, }
      return render_to_response('invites/invite_form.html', context, context_instance=RequestContext(request))
  else:
    form = InviteForm(instance=invite, prefix="invite")
    context = { 'invite_form': form, }
    return render_to_response('invites/invite_form.html', context, context_instance=RequestContext(request))