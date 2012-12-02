from django.shortcuts import render_to_response

from ninetyseven.apps.invites.models import *

def check_invite_key(view):
  """
  This decorator returns the login view if the activation key is found.
  If not, it returns an invalid template.
  """
  def inner(request):
    if not request.POST:
      activation_key = request.GET.get('activation_key', None)
      try:
        invite = Invite.objects.get(activation_key=activation_key)
        return view(request)
      except Invite.DoesNotExist:
        return render_to_response("invites/invalid_activation_key.html", {})
    else:
      return view(request)
  return inner