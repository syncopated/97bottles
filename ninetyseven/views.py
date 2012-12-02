from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.db import models
from django.views.generic.list_detail import object_list, object_detail
from django.core.cache import cache
from django.core.mail import send_mail
import subprocess
import random

from savoy.core.new.profiles.models import Profile
from savoy.utils.importers import getjson, getxml

from ninetyseven.apps.beers.forms import *
from ninetyseven.apps.tell_a_friend.forms import *

Relationship = models.get_model('relationships', 'relationship')
City = models.get_model('geo', 'city')
Beer = models.get_model('beers', 'beer')
Review = models.get_model('reviews','review')
UserRecommendation = models.get_model("beers","userrecommendation")

def homepage(request, template_name="homepage.html"):
  """ Returns the view for the homepage. """
  interesting_beers   = Beer.objects.all().order_by('-interestingness')[:20]
  interesting_beer    = interesting_beers[random.randint(0, 19)]
  most_recent_reviews = Review.objects.order_by('-date_created')[:7]
  if not request.user.is_anonymous():
    interesting_beer_user_recommendation = UserRecommendation(from_user=request.user, beer=interesting_beer)
    interesting_beer_user_recommendation_form = UserRecommendationForm(user=request.user, beer=interesting_beer, instance=interesting_beer_user_recommendation)
  else:
    interesting_beer_user_recommendation = None
    interesting_beer_user_recommendation_form = None
  context = {
    'interesting_beer': interesting_beer, 
    'interesting_beer_user_recommendation_form': interesting_beer_user_recommendation_form,
    'most_recent_reviews': most_recent_reviews,
  }
  return render_to_response(template_name, RequestContext(request, context))

def people_index(request, template_name='profiles/people_index.html', template_object_name="profile", extra_context={}):
  """
  Returns the view for the main people page.
  """
  if not request.user.is_anonymous():
    return render_to_response(template_name, RequestContext(request, { 'profile': request.user.profile }))
  else:
    return render_to_response(template_name, RequestContext(request, {}))


def profile_detail(request, username):
  user = get_object_or_404(User, username=username)
  try:
    profile = Profile.objects.get(user=user)
  except Profile.DoesNotExist:
    profile = Profile.objects.create_or_update(instance=user)
  context = { 'profile': profile, 'tell_a_friend_form': TellAFriendForm(), 'suckit': "suck" }
  return render_to_response('profiles/profile_detail.html', context, context_instance=RequestContext(request))


def user_beers_recommended(request, username, template_name='profiles/beers_recommended.html'):
  """ Returns a generic list view including a list of beers recommended for a particular user. """
  user = get_object_or_404(User, username=username)
  user_recommendations       = UserRecommendation.objects.filter(to_user=user, dismissed=False)
  recommended_beers_by_users = user.info.recommended_beers_by_users()
  recommended_beers_by_tags  = user.info.recommended_beers_by_tags()
  return render_to_response(template_name, RequestContext(request, { 'profile': user.profile, 'user_recommendations': user_recommendations, 'recommended_beers_by_tags': recommended_beers_by_tags, 'recommended_beers_by_users': recommended_beers_by_users, }))
  
def user_beers_added(request, username, template_name='profiles/beers_added.html', template_object_name="beer", extra_context={}):
  """ Returns a generic list view including a list of beers a particular user has added to the site. """
  user = get_object_or_404(User, username=username)
  extra = { 'profile': user.profile }
  extra.update(extra_context)
  return object_list(
    request,
    queryset = Beer.objects.filter(created_by=user),
    template_name = template_name,
    template_object_name = template_object_name,
    extra_context = extra,
  )
  
def user_reviews_added(request, username, template_name='profiles/reviews_added.html', template_object_name="review", extra_context={}):
  """ Returns a generic list view including a list of reviews a particular user has added to the site. """
  user = get_object_or_404(User, username=username)
  extra = { 'profile': user.profile }
  extra.update(extra_context)
  return object_list(
    request,
    queryset = Review.objects.filter(created_by=user),
    template_name = template_name,
    template_object_name = template_object_name,
    extra_context = extra,
  )

def top_contributors(request, template_name='profiles/top_contributors.html', template_object_name="profile", extra_context={}):
  """ Returns a generic list view including the profile object for the top 100 contributors on the site. """
  top_contributors = User.objects.all().order_by('-info__contribution_score')
  return render_to_response(template_name, RequestContext(request, { 'user_list': top_contributors[:100], }))
  
  
def new_users(request, template_name='profiles/new_users.html', template_object_name="profile", extra_context={}):
  """ Returns a generic list view including the profile object for the 100 newest users on the site. """
  noobs = User.objects.all().order_by('-date_joined')
  return render_to_response(template_name, RequestContext(request, { 'user_list': noobs[:100], }))


def search_cities(request):
  template = 'geo/city_search.html'
  context = {}
  if request.GET.__contains__('parent_form'):
    parent_form = request.GET['parent_form']
  else:
    parent_form = None
  if request.GET.__contains__('search'):
    query = request.GET['search']
    cities = City.objects.filter(city__icontains=query)
    if request.is_ajax():
      template = 'geo/city_search_ajax.html'
      if not len(query) > 2:
        cities = []
    context = {'city_list': cities, 'parent_form': parent_form}
    return render_to_response(template, context, context_instance=RequestContext(request))
  else:
    raise Http404("You did not enter search terms.")

def find_twitter_friends(request, template_name="profiles/find_friends.html"):
  """
  Very simple Twitter friend finder. Not a very robust method, 
  but it'll work until Twitter gets oAuth going.
  """
  if request.GET.__contains__('username'):
    service_username = request.GET['username']
    service_user_info_url = "http://twitter.com/users/show/%s.xml" % service_username
    service_user_info = getxml(service_user_info_url)
    try:
      friend_count = int(service_user_info.find('friends_count').text)
    except AttributeError:
      raise Http404("No friend count. This probably means our Twitter API limit has been reached for this hour.")
    if friend_count:
      page_range = range(1, friend_count/100+2)
      friend_screennames = []
      for page in page_range:
        service_friends_url = "http://twitter.com/statuses/friends/%s.json?page=%s" % (service_username, page)
        service_friends = getjson(service_friends_url)
        service_friends_screennames = friend_screennames.extend(friend['screen_name'] for friend in service_friends)
      users = User.objects.filter(username__in=friend_screennames)
      return render_to_response(template_name, RequestContext(request, { 'friend_list': users, }))
  else:
    return render_to_response(template_name, RequestContext(request, { }))
  
    