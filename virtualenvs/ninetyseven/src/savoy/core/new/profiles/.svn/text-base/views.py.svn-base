from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect
from django.views.generic import list_detail
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from savoy.core.new.profiles.models import *
from savoy.core.new.profiles.forms import *


def profile_list(request):
    return list_detail.object_list(
        request,
        template_object_name = "profile",
        queryset = Profile.objects.all(),
    )
profile_list.__doc__ = list_detail.object_list.__doc__


def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    try:
      profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
      profile = Profile.objects.create_or_update(instance=user)
    context = { 'profile':profile }
    return render_to_response('profiles/profile_detail.html', context, context_instance=RequestContext(request))
 

@login_required
def profile_edit(request, template_name='profiles/profile_form.html', profile_form_class=ProfileForm, user_form_class=UserForm):
    """Edit profile."""

    if request.POST:
        profile = Profile.objects.get(user=request.user)
        profile_form = profile_form_class(request.POST, request.FILES, instance=profile, prefix="profile")
        city_form = CityForm(request.POST, prefix="city")
        user_form = user_form_class(request.POST, instance=request.user, prefix="user")
        service_formset = ServiceFormSet(request.POST, instance=profile)
        link_formset = LinkFormSet(request.POST, instance=profile)
        
        if profile_form.is_valid() and user_form.is_valid() and service_formset.is_valid() and link_formset.is_valid():
            city = None
            new_city = None
            existing_city = None
            if city_form.is_valid():
              if request.POST['city-city'] != "":
                # The city form was valid and had data entered, so let's save the city.
                new_city = city_form.save()
            if request.POST['profile-city'] != '':
              # This user is from an existing city; get the city from the database.
              existing_city = City.objects.get(id=int(request.POST['profile-city']))
            profile = profile_form.save(commit=False)
            if existing_city:
              profile.city = existing_city
            if new_city:
              profile.city = new_city
            profile.save()
            
            user_form.save()
            service_formset.save()
            link_formset.save()
            return HttpResponseRedirect(reverse('profile_detail', args=(request.user.username,)))
        else:
            context = {
                'city_form': city_form,
                'profile_form': profile_form, 
                'user_form': user_form,
                'service_formset': service_formset,
                'link_formset': link_formset,
                'profile': profile,
            }
    else:
        try:
          profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
          profile = Profile.objects.create_or_update(instance=request.user)
        service_formset = ServiceFormSet(instance=profile)
        link_formset = LinkFormSet(instance=profile)
        context = {
            'city_form': CityForm(prefix="city"),
            'profile_form': profile_form_class(instance=profile, prefix="profile"), 
            'user_form': user_form_class(instance=request.user, prefix="user"),
            'service_formset': service_formset,
            'link_formset': link_formset,
            'profile': profile,
        }
    return render_to_response(template_name, context, context_instance=RequestContext(request))