from django.conf.urls.defaults import *
from django.db import models

from ninetyseven.apps.beers.views import *
from ninetyseven.apps.beers.forms import *

urlpatterns = patterns('',
  url(
    regex = r'^beer/_user_recommendations/submit/(?P<beer_id>\d+)/$',
    view = user_recommendation_submit,
    name = 'user_recommendation_submit',
  ),
  url(
    regex = r'^beer/_user_recommendations/approve/(?P<user_recommendation_id>\d+)/$',
    view = user_recommendation_approve,
    name = 'user_recommendation_approve',
  ),
  url(
    regex = r'^beer/_user_recommendations/dismiss/(?P<user_recommendation_id>\d+)/$',
    view = user_recommendation_dismiss,
    name = 'user_recommendation_dismiss',
  ),
  url(
    regex = r'^beer/_recently_added/$',
    view = recently_added_beers,
    name = 'recently_added_beers',
  ),
  url(
    regex = r'^beer/_top_rated/$',
    view = top_rated_beers,
    name = 'top_rated_beers',
  ),
  url(
    regex = r'^beer/_most_interesting/$',
    view = most_interesting_beers,
    name = 'most_interesting_beers',
  ),
  url(
    regex = r'^beer/_add/$',
    view = add_beer,
    name = 'add_beer',
  ),
  url(
    regex = r'^beer/_edit/(?P<beer_id>\d+)/$',
    view = edit_beer,
    name = 'edit_beer',
  ),
  url(
    regex = r'^beer/_search/$',
    view = search_beer,
    name = 'search_beer',
  ),
  url(
    regex = r'^beer/_skunky/$',
    view = award_beer_list,
    name = 'award_beer_list_skunky',
    kwargs = {
      'queryset': Beer.skunky.all(),
      'award': { 'slug': 'skunky', 'name': 'Skunky' },
    }
  ),
  url(
    regex = r'^beer/_girlie/$',
    view = award_beer_list,
    name = 'award_beer_list_girlie',
    kwargs = {
      'queryset': Beer.girlie.all(),
      'award': { 'slug': 'girlie', 'name': 'Chicks dig it!' },
    }
  ),
  url(
    regex = r'^beer/_high-rated/$',
    view = award_beer_list,
    name = 'award_beer_list_high-rated',
    kwargs = {
      'queryset': Beer.high_rated.all(),
      'award': { 'slug': 'high-rated', 'name': 'Awesome!' },
    }
  ),
  url(
    regex = r'^beer/_staff-pick/$',
    view = award_beer_list,
    name = 'award_beer_list_staff-pick',
    kwargs = {
      'queryset': Beer.staff_pick.all(),
      'award': { 'slug': 'staff-pick', 'name': 'Staff pick' },
    }
  ),
  url(
    regex = r'^beer/_high-alcohol/$',
    view = award_beer_list,
    name = 'award_beer_list_high-alcohol',
    kwargs = {
      'queryset': Beer.high_alcohol.all(),
      'award': { 'slug': 'high-alcohol', 'name': 'High alcohol' },
    }
  ),
  url(
    regex = r'^beer/_hoppy/$',
    view = award_beer_list,
    name = 'award_beer_list_hoppy',
    kwargs = {
      'queryset': Beer.hoppy.all(),
      'award': { 'slug': 'hoppy', 'name': 'Hoppy' },
    }
  ),
  url(
    regex = r'^beer/_session/$',
    view = award_beer_list,
    name = 'award_beer_list_session',
    kwargs = {
      'queryset': Beer.session.all(),
      'award': { 'slug': 'session', 'name': 'Session' },
    }
  ),
  url(
    regex = r'^beer/_feeling_lucky/$',
    view  = feeling_lucky,
    name  = 'feeling_lucky', 
  ),
  url(
    regex = r'^(?P<slug>[-\w]+)/$',
    view = hierarchy_detail,
    name = 'hierarchy_detail',
  ),
  url(
    regex = r'^(?P<path>[-\w\/]+)/$',
    view = category_detail,
    name = 'category_detail',
  ),
)