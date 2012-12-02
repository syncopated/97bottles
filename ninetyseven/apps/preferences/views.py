from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect
from django.views.generic import list_detail
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from ninetyseven.apps.preferences.models import *
from ninetyseven.apps.preferences.forms import *

@login_required
def preferences_edit(request, template_name='preferences/preference_form.html'):
  """Edit preferences."""
  profile = request.user.profile
  if request.POST:
    preference = UserPreference.objects.get(user=request.user)
    preference_form = UserPreferenceForm(request.POST, request.FILES, instance=preference)

    if preference_form.is_valid():
      preference_form.save()
      return HttpResponseRedirect(reverse('preferences_edit'))
    else:
      context = { 'preference_form': preference_form, 'profile': profile }
  else:
    try:
      preference = UserPreference.objects.get(user=request.user)
    except UserPreference.DoesNotExist:
      preference = UserPreference.objects.create_or_update(instance=request.user)
    context = { 'preference_form': UserPreferenceForm(instance=preference), 'profile': profile }
  return render_to_response(template_name, context, context_instance=RequestContext(request))