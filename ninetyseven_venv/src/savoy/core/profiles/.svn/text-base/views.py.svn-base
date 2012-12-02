from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.forms.models import model_to_dict
from django.template import RequestContext
from django.shortcuts import render_to_response

from savoy.core.profiles.models import Profile
from savoy.core.profiles.forms import *

def profile_detail(request, username):
  from django.views.generic.list_detail import object_detail
  
  try:
    user      = User.objects.get(username=username)
    profile   = Profile.objects.get(user=user)
  except:
    raise Http404

  return object_detail(
    request, 
    queryset              = Profile.objects.all(),
    object_id             = profile.user.id,
    template_object_name  = 'profile',
  )  
  

def edit_profile(request, username):
  try:
    user      = User.objects.get(username=username)
    profile   = Profile.objects.get(user=user)
  except:
    raise Http404
  
  # Ensure the user is trying to edit their own profile, and not someone else's.
  if request.user != user:
    return HttpResponseForbidden("You may not edit another user's profile.")
  
  if request.method == 'POST':
    # If there is post data, the user has already filled out the forms -- process them.
    user_form             = UserForm(instance=user, data=request.POST)
    profile_form          = ProfileForm(instance=profile, data=request.POST)
    
    # Check the form for validity
    if user_form.is_valid() and profile_form.is_valid():
      user                = user_form.save()
      profile             = profile_form.save()
      # Redirect the user to their own profile.
      return HttpResponseRedirect(profile.get_absolute_url())
    else:
      # If it's not valid, return the form again (with errors).
      context             = RequestContext(request, { 'user_form': user_form, 'profile_form': profile_form })
      return render_to_response('profile/profile_form.html', context)
      
  else:
    # If there is no post data, we don't need to process the forms -- just display them.
    user_form             = UserForm(instance=user, data=model_to_dict(user))
    profile_form          = ProfileForm(instance=profile, data=model_to_dict(profile))
    context               = RequestContext(request, { 'user_form': user_form, 'profile_form': profile_form })
    return render_to_response('profiles/profile_form.html', context)