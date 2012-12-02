import datetime
from random import randint

from django.views.generic.list_detail import object_detail, object_list
from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core import serializers
from django.utils import simplejson
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.template.defaultfilters import dictsort

from categorization.models import *
from categorization.views import *
from faves.models import *

from savoy.core.geo.models import City
from savoy.core.constants import COUNTRY_CHOICES

from ninetyseven.apps.beers.models import *
from ninetyseven.apps.beers.forms import *

def unique(thelist):
  uniquedict = {}
  for i in thelist:
    uniquedict[i] = 0
  return uniquedict.keys()

### Brewery views

def brewery_index(request, template_name='breweries/brewery_index.html', template_object_name="brewery", extra_context={}):
  cities_with_breweries = City.objects.filter(breweries__isnull=False).distinct()
  countries = []
  for city in cities_with_breweries:
    for country in COUNTRY_CHOICES:
      if country[0] == city.country:
        country_dict = { 'code': city.country, 'name': country[1]  }
        if country_dict not in countries:
          countries.append(country_dict)
        break
  extra = { 'country_list': countries }
  extra.update(extra_context)
  return object_list(
    request,
    queryset = Brewery.objects.all(),
    template_name = template_name,
    template_object_name = template_object_name,
    extra_context = extra,
  )

def brewery_country_detail(request, country, template_name='breweries/country_detail.html', template_object_name="city", extra_context={}):
  try:
    cities = City.objects.filter(country=country, breweries__isnull=False).distinct()
  except:
    raise Http404  
  for country_code in COUNTRY_CHOICES:
    if country_code[0] == country:
      country_name = country_code[1]
  
  if country == "us":
    states = City.objects.filter(country=country, breweries__isnull=False).distinct().values('state').distinct()
  else:
    states = City.objects.filter(country=country, breweries__isnull=False).distinct().values('province').distinct()
  state_list = []
  for state in states:
    if country == "us":
      state = state['state']
      state_dict = { 'name': cities.filter(state=state)[0].get_state_display(), 'url': cities.filter(state=state)[0].get_state_url(), 'code': state.lower() }
    else:
      province = state['province']
      try:
        province_url = cities.filter(province=province)[0].get_state_url()
      except:
        province_url = ''
      state_dict = { 'name': province, 'url': province_url, 'code': province.lower() }
    state_list.append(state_dict)
  
  extra = {
    'country': country_name,
    'country_code': country.upper(),
    'brewery_list': Brewery.objects.filter(city__in=cities),
    'state_list': dictsort(state_list, 'name'),
  }
  
  extra.update(extra_context)
  return object_list(
    request, 
    queryset = cities,
    template_name = template_name,
    template_object_name = template_object_name,
    allow_empty = False,
    extra_context = extra,
  )


def brewery_state_detail(request, country, state, template_name='breweries/state_detail.html', template_object_name="city", extra_context={}):
  from django.template.defaultfilters import slugify
  cities = City.objects.filter(slug__endswith=slugify(state + " " + country), breweries__isnull=False).distinct()
  try:
    # This needs to raise an exception on things like /ca/vancouver, but not on /ca/bc/vancouver.
    if slugify(cities[0].city) == state:
      raise Exception
  except:
    try:
      # If not, this is probably supposed to be a city view, not a state view.
      city = state
      return brewery_city_detail(request=request, country=country, city=city)
    except:
      raise Http404
  country_name  = cities[0].get_country_display()
  country_code  = cities[0].country
  if country == "us":
    state_name  = cities[0].get_state_display()
    state_code  = cities[0].state
  else:
    state_name  = cities[0].province
    state_code  = slugify(cities[0].province)
  extra = {
    'country': country_name,
    'country_code': country_code,
    'state': state_name,
    'state_code': state_code,
    'brewery_list': Brewery.objects.filter(city__in=cities),
  }
  extra.update(extra_context)
  return object_list(
    request, 
    queryset = cities,
    template_name = template_name,
    template_object_name = template_object_name,
    allow_empty=True,
    extra_context = extra,
  )

def brewery_city_detail(request, country, city, state=None, allow_empty=True, template_name='breweries/city_detail.html', template_object_name="city", extra_context={}):
  from django.template.defaultfilters import slugify
  if state:
    slug = slugify(city + " " + state + " " + country)
  else:
    slug = slugify(city + " " + country)
  try:
    city = City.objects.get(slug=slug)
  except City.DoesNotExist:
    return brewery_detail(request=request, country=country, city=state, brewery_slug=city)
  country_name  = city.get_country_display()
  country_code  = city.country
  if country == "us":
    state_name  = city.get_state_display()
    state_code  = city.state
  else:
    state_name  = city.province
    state_code  = slugify(city.province)
  extra = {
    'country': country_name,
    'country_code': country_code,
    'state': state_name,
    'state_code': state_code,
    'brewery_list': Brewery.objects.filter(city=city),
  }
  extra.update(extra_context)
  return object_detail(
    request, 
    queryset = City.objects.all(),
    template_name = template_name,
    template_object_name = template_object_name,
    slug_field = 'slug',
    slug = slug,
    extra_context = extra,
  )


def brewery_detail(request, country, city, brewery_slug, state=None, allow_empty=True, template_name='breweries/brewery_detail.html', template_object_name="brewery", extra_context={}):
  from django.template.defaultfilters import slugify
  if state:
    slug = slugify(city + " " + state + " " + country)
  else:
    slug = slugify(city + " " + country)
  city = get_object_or_404(City, slug=slug)
  brewery = get_object_or_404(Brewery, city=city, slug=brewery_slug)
  extra = {}
  extra.update(extra_context)
  return object_detail(
    request,
    template_name = template_name,
    template_object_name = template_object_name,
    slug = brewery_slug,
    slug_field = 'slug',
    queryset = Brewery.objects.filter(city=city),
    extra_context = extra,
  )

@login_required
def edit_brewery(request, brewery_id, template_name='breweries/edit_brewery.html', template_object_name="brewery"):
  """ Displays a form for editing an existing brewery. """
  brewery = get_object_or_404(Brewery, id=brewery_id)
  if request.method == 'POST':
    brewery_form = EditBreweryForm(request.POST, instance=brewery, prefix="brewery")
    if not brewery_form.is_valid():
      # The form is not valid; return the form to the user.
      context = { 'brewery_form': brewery_form, 'brewery': brewery, }
      return render_to_response(template_name, context, context_instance=RequestContext(request))
    else:
      brewery = brewery_form.save(commit=False)
      brewery.updated_by = request.user
      brewery.date_updated = datetime.datetime.now()
      brewery.save()
      return HttpResponseRedirect(brewery.get_absolute_url())
  else:
    # No post data, so we should give the user a form.
    brewery_form = EditBreweryForm(instance=brewery, prefix="brewery")
    context = { 'brewery_form': brewery_form, 'brewery': brewery, }
    return render_to_response(template_name, context, context_instance=RequestContext(request))
    

def search_breweries(request):
  template = 'breweries/brewery_search.html'
  context = {}
  if request.GET.__contains__('search'):
    query = request.GET['search']
    breweries = Brewery.objects.filter(name__icontains=query)
    context = {'brewery_list': breweries,}
    if request.is_ajax():
      template = 'breweries/brewery_search_ajax.html'
  return render_to_response(template, context, context_instance=RequestContext(request))
    



### Beer views

def beer_detail(request, country, city, brewery_slug, slug, state=None, template_name='beers/beer_detail.html', template_object_name="beer", extra_context={}):
  """
  Displays an individual beer, or renders the category view if this is not a beer.
  """
  from ninetyseven.apps.beers.models import UserRecommendation
  
  brewery = get_object_or_404(Brewery, slug=brewery_slug)
  beer = get_object_or_404(Beer, brewery=brewery, slug=slug)
  category = beer.variety
  if not request.user.is_anonymous():
    user_recommendation = UserRecommendation(from_user=request.user, beer=beer)
    user_recommendation_form = UserRecommendationForm(user=request.user, beer=beer, instance=user_recommendation)
  else:
    user_recommendation = None
    user_recommendation_form = None
  extra = { 'category': category, 'user_recommendation_form': user_recommendation_form }
  extra.update(extra_context) 
  return object_detail(
    request,
    template_name = template_name,
    template_object_name = template_object_name,
    extra_context = extra,
    slug = slug,
    slug_field = 'slug',
    queryset = Beer.objects.all(),
  )

def reviews_for_beer(request, country, city, brewery_slug, slug, state=None, template_name='beers/beer_reviews.html', template_object_name="beer", extra_context={}):
  """ Displays a list of reviews for a particular beer (this is primarily for use on the mobile site.) """
  brewery = get_object_or_404(Brewery, slug=brewery_slug)
  beer = get_object_or_404(Beer, brewery=brewery, slug=slug)
  category = beer.variety
  extra = { 'category': category, 'review_list': Review.objects.filter(beer=beer, is_removed=False) }
  extra.update(extra_context) 
  extra.update(extra_context) 
  return object_detail(
    request,
    template_name = template_name,
    template_object_name = template_object_name,
    extra_context = extra,
    slug = slug,
    slug_field = 'slug',
    queryset = Beer.objects.all(),
  )

def feeling_lucky(request):
  num_of_beers = Beer.objects.count()
  random_beer = Beer.objects.all()[randint(0, num_of_beers-1)]
  return HttpResponseRedirect(random_beer.get_absolute_url())


@login_required
def edit_beer(request, beer_id, template_name='beers/edit_beer.html', template_object_name="beer"):
  """ Displays a form for editing an existing beer. """
  beer = get_object_or_404(Beer, id=beer_id)
  brewery = beer.brewery
  colors = BeerColor.objects.all()
  if request.method == 'POST':
    beer_form = EditBeerForm(request.POST, instance=beer, prefix="beer")
    if not beer_form.is_valid():
      # The form is not valid; return the form to the user.
      context = { 'beer_form': beer_form, 'beer': beer, 'colors': colors }
      return render_to_response(template_name, context, context_instance=RequestContext(request))
    else:
      beer = beer_form.save(commit=False)
      beer.updated_by = request.user
      beer.date_updated = datetime.datetime.now()
      beer.save()
      return HttpResponseRedirect(beer.get_absolute_url())
  else:
    # No post data, so we should give the user a form.
    beer_form = EditBeerForm(instance=beer, prefix="beer")
    context = { 'beer_form': beer_form, 'beer': beer, 'colors': colors }
    return render_to_response(template_name, context, context_instance=RequestContext(request))
  

@login_required
def add_beer(request):
  colors = BeerColor.objects.all()
  if request.method == 'POST':
    # We've got data. Let's process the forms.
    beer_form = BeerForm(request.POST, prefix="beer")
    brewery_form = BreweryForm(request.POST, prefix="brewery")
    city_form = CityForm(request.POST, prefix="city")
    if not beer_form.is_valid() or not brewery_form.is_valid():
      # One of the two forms is not valid; return the form to the user.
      context = {'beer_form': beer_form, 'brewery_form': brewery_form, 'city_form': city_form, 'colors': colors }
      return render_to_response('beers/beer_form.html', context, context_instance=RequestContext(request))
    else:
      # The forms should be valid, so let's process data.
      brewery = None
      city = None
      if city_form.is_valid():
        if request.POST['city-city'] != "":
          # The city form was valid and had data entered, so let's save the city.
          city = city_form.save(commit=False)
          city.save()
      if request.POST['brewery-city'] != '':
        # This brewery is from an existing city; get the city from the database.
        city = City.objects.get(id=int(request.POST['brewery-city']))
      if brewery_form.is_valid():
        if request.POST['brewery-name'] != "":
          # The brewery form was valid and had data entered, so let's save the brewery.
          brewery = brewery_form.save(commit=False)
          brewery.created_by = request.user
          if city:
            brewery.city = city
          else:
            # The user did not select or add a city for the brewery. Add the error to the error dict
            # and then return the form to the user.
            brewery_form.errors['city'] = "You must either select or add a city."
            context = {'beer_form': beer_form, 'brewery_form': brewery_form, 'city_form': city_form, 'colors': colors }
            return render_to_response('beers/beer_form.html', context, context_instance=RequestContext(request))
          brewery.save()
      else:
        raise Exception("Brewery form was no valid")
      if request.POST['beer-brewery'] != '':
        # This beer is from an existing brewery; get the brewery from the database.
        brewery = Brewery.objects.get(id=int(request.POST['beer-brewery']))
      if beer_form.is_valid():
        # The beer form was valid, so let's save the beer.
        beer = beer_form.save(commit=False)
        beer.created_by = request.user
        if brewery:
          beer.brewery = brewery
        else:
          # The user did not select or add a brewery. Add the error to the error dict
          # and then return the form to the user.
          beer_form.errors['brewery'] = "You must either select or add a brewery."
          context = {'beer_form': beer_form, 'brewery_form': brewery_form, 'city_form': city_form, 'colors': colors }
          return render_to_response('beers/beer_form.html', context, context_instance=RequestContext(request))
        beer.save()
      # We're good. Send the user to the success page.
      context = { 'beer': beer, 'brewery': brewery }
      return render_to_response('beers/beer_form_success.html', context, context_instance=RequestContext(request))
  else:
    # No post data, so we should give the user an empty form.
    beer_form = BeerForm(instance=Beer(), prefix="beer")
    brewery_form = BreweryForm(instance=Brewery(), prefix="brewery")
    city_form = CityForm(instance=City(), prefix="city")
    context = { 'beer_form': beer_form, 'brewery_form': brewery_form, 'city_form': city_form, 'colors': colors }
    return render_to_response('beers/beer_form.html', context, context_instance=RequestContext(request))
  
def search_beer(request):
  template = 'beers/beer_search.html'
  context = {}
  if request.GET.__contains__('search'):
    query = request.GET['search']
    beers = Beer.objects.filter(Q(name__icontains=query) | Q(brewery__name__icontains=query))
    if request.is_ajax():
      template = 'beers/beer_search_ajax.html'
      if not len(query) > 2:
        beers = []
    context = {'beer_list': beers,}
  return render_to_response(template, context, context_instance=RequestContext(request))

def award_beer_list(request, template_name='beers/award_beer_list.html', template_object_name="beer", queryset=Beer.objects.all(), award=None, extra_context={}):
  """ Returns a generic list view including a list of beers added to the site, ordered by reverse creation date. """
  extra = { 'award': award }
  extra.update(extra_context)
  return object_list(
    request,
    queryset = queryset,
    template_name = template_name,
    template_object_name = template_object_name,
    extra_context = extra,
  )

def recently_added_beers(request, template_name='beers/recently_added.html', template_object_name="beer", extra_context={}):
  """ Returns a generic list view including a list of beers added to the site, ordered by reverse creation date. """
  extra = { }
  extra.update(extra_context)
  return object_list(
    request,
    queryset = Beer.objects.all().order_by('-date_created')[:100],
    template_name = template_name,
    template_object_name = template_object_name,
    extra_context = extra,
  )
  
def top_rated_beers(request, template_name='beers/top_rated.html', template_object_name="beer", extra_context={}):
  """ Returns a generic list view including a list of beers added to the site, ordered by rating. """
  extra = { }
  extra.update(extra_context)
  return object_list(
    request,
    queryset = Beer.objects.all().order_by('-rating')[:100],
    template_name = template_name,
    template_object_name = template_object_name,
    extra_context = extra,
  )
  
def most_interesting_beers(request, template_name='beers/most_interesting.html', template_object_name="beer", extra_context={}):
  """ Returns a generic list view including a list of beers added to the site, ordered by interestingness. """
  extra = { }
  extra.update(extra_context)
  return object_list(
    request,
    queryset = Beer.objects.all().order_by('-interestingness')[:100],
    template_name = template_name,
    template_object_name = template_object_name,
    extra_context = extra,
  )
  
  
# User recommendation views

def user_recommendation_submit(request, beer_id, email_body_template='beers/user_recommendation_email_body.txt', email_subject_template='beers/user_recommendation_email_subject.txt', mimetype='text/html'):
  if request.method == 'POST':
    beer_content_type = ContentType.objects.get_for_model(Beer)
    beer = Beer.objects.get(id=beer_id)
    user_recommendation = UserRecommendation(from_user=request.user, beer=beer)
    user_recommendation_form = UserRecommendationForm(data=request.POST, user=request.user, beer=beer, instance=user_recommendation)
    if user_recommendation_form.is_valid():
      user_recommendation = user_recommendation_form.save(commit=False)
      user_recommendation.date_created = datetime.datetime.now()
      message = "Your recommendation was successfully sent to %s." % user_recommendation.to_user.profile.name
      user_recommendation.save()
      request.user.message_set.create(message=message)
      
      if user_recommendation.to_user.preferences.email_notification:
        site = Site.objects.get(pk=settings.SITE_ID)
        context = {
          'user_recommendation': user_recommendation,
          'site': site
        }
        subject = render_to_string(email_subject_template, context)
        message = render_to_string(email_body_template, context)
        if user_recommendation.to_user.email:
          email = EmailMessage(subject, message, settings.REPLY_EMAIL, ['%s' % user_recommendation.to_user.email])
          email.send(fail_silently=False)
      
      return HttpResponseRedirect(user_recommendation.beer.get_absolute_url())
    else:
      message = "There was an error sending your recommendation. Please try again."
      return HttpResponseRedirect(user_recommendation.beer.get_absolute_url())
  else:
    raise Http500("This page only accepts POSTs.")
    
def user_recommendation_approve(request, user_recommendation_id):
  user_recommendation = get_object_or_404(UserRecommendation, id=user_recommendation_id)
  if request.user == user_recommendation.to_user:
    fave_type = FaveType.objects.get(slug="to-dos")
    fave = Fave.objects.create_or_update(user_recommendation.to_user, user_recommendation.beer, fave_type, force_not_withdrawn=True)
    user_recommendation.dismissed = True
    user_recommendation.save()
    message = "%s has been added to your To-drink list." % user_recommendation.beer.name
    request.user.message_set.create(message=message)
    return HttpResponseRedirect(reverse('user_beers_recommended', args=[request.user]))
  else:
    raise Http500("You do not have permission to access this page.")
  
  
def user_recommendation_dismiss(request, user_recommendation_id):
  user_recommendation = get_object_or_404(UserRecommendation, id=user_recommendation_id)
  if request.user == user_recommendation.to_user:
    fave_type = FaveType.objects.get(slug="no-thanks")
    fave = Fave.objects.create_or_update(user_recommendation.to_user, user_recommendation.beer, fave_type, force_not_withdrawn=True)
    user_recommendation.dismissed = True
    user_recommendation.save()
    message = "Your recommendation has been archived and %s has been added to your no-thanks list." % user_recommendation.beer.name
    request.user.message_set.create(message=message)
    return HttpResponseRedirect(reverse('user_beers_recommended', args=[request.user]))
  else:
    raise Http500("You do not have permission to access this page.")