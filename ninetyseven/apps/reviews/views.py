import datetime

from django.db import models
from django.template import RequestContext
from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.views.generic.list_detail import object_detail, object_list
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator

from faves.models import *

from ninetyseven.apps.reviews.models import *
from ninetyseven.apps.reviews.forms import *
from ninetyseven.apps.beers.forms import *

@login_required
def post_review(request):
  if request.method == 'POST':
    beer = Beer.objects.get(id=request.POST['beer'])
    user = request.user
    try:
      # See if the user already has posted a review of this beer.
      # If so, edit this review instance, instead of posting an entirely new review.
      # This prevents review spamming.
      review = Review.objects.get(created_by=user, beer=beer)
      review_form = ReviewForm(request.POST, instance=review, prefix="review")
    except Review.DoesNotExist:
      review_form = ReviewForm(request.POST, prefix="review")
    
    new_city = None
    existing_city = None
    city_form = CityForm(request.POST, prefix="city")
    
    if request.POST['review-city'] != '':
      # This review is from an existing city; get the city from the database.
      existing_city = City.objects.get(id=int(request.POST['review-city']))
      
    if city_form.is_valid():
      if request.POST['city-city'] != "":
        # The city form was valid and had data entered, so let's save the city.
        new_city = city_form.save(commit=False)
        new_city.save()
    
    if review_form.is_valid():
      review = review_form.save(commit=False)
      review.created_by = user
      review.beer = beer
      if new_city:
        review.city = new_city
      elif existing_city:
        review.city = existing_city
      else:
        review.city = None
      review.ip_address = request.META.get("REMOTE_ADDR", None)
      review.save()
    else:
      context = {
        'city_form': city_form,
        'review_form': review_form,
        'beer': beer,
      }
      return render_to_response('reviews/review_preview.html', context, context_instance=RequestContext(request))
    context = {
      'review': review,
      'beer': beer,
    }
    
    # If the beer was in the user's to-drink list, remove it.
    try:
      beer_content_type = ContentType.objects.get_for_model(Beer)
      fave = Fave.objects.get(type__slug="to-dos", content_type=beer_content_type, object_id=beer.id, user=request.user)
      fave.withdrawn = True
      fave.save()
    except:
      pass
    return HttpResponseRedirect(review.get_absolute_url())
  else:
    raise Http500("This page only accepts POSTs.")  
    

@login_required
def edit_review(request, review_id, template_name='reviews/edit_review.html', template_object_name="review"):
  """ Displays a form for editing an existing beer. """
  review = get_object_or_404(Review, id=review_id)
  
  data = request.POST.copy()
  delete = "delete" in data
  if delete:
    beer_url = review.beer.get_absolute_url()
    review.delete()
    return HttpResponseRedirect(beer_url)
  
  if review.created_by == request.user or request.user.is_staff:
    beer = review.beer
    if request.method == 'POST':
      review_form = ReviewForm(request.POST, instance=review, prefix="review")
      
      new_city = None
      existing_city = None
      city_form = CityForm(request.POST, prefix="city")
      
      if request.POST['review-city'] != '':
        # This review is from an existing city; get the city from the database.
        existing_city = City.objects.get(id=int(request.POST['review-city']))

      if city_form.is_valid():
        if request.POST['city-city'] != "":
          # The city form was valid and had data entered, so let's save the city.
          new_city = city_form.save(commit=False)
          new_city.save()
      
      if not review_form.is_valid():
        # The form is not valid; return the form to the user.
        context = { 'review': review, 'review_form': review_form, 'city_form': city_form, 'beer': beer, }
        return render_to_response(template_name, context, context_instance=RequestContext(request))
      else:
        review = review_form.save(commit=False)
        review.updated_by = request.user
        review.date_updated = datetime.datetime.now()
        review.save()
        return HttpResponseRedirect(review.get_absolute_url())
    else:
      # No post data, so we should give the user a form.
      city_form = CityForm(prefix="city")
      review_form = ReviewForm(instance=review, prefix="review")
      context = { 'review': review, 'review_form': review_form, 'beer': beer, 'city_form': city_form}
      return render_to_response(template_name, context, context_instance=RequestContext(request))
  else:
    raise Http404("You can only edit your own reviews.")

def recently_added_reviews(request, template_name='reviews/recently_added.html', template_object_name="review", extra_context={}):
  """ Returns a generic list view including a list of reviews added to the site, ordered by reverse creation date. """
  extra = { }
  extra.update(extra_context)
  return object_list(
    request,
    queryset = Review.objects.all().order_by('-date_created'),
    template_name = template_name,
    template_object_name = template_object_name,
    extra_context = extra,
  )
 
def get_more_reviews(request):
    """
    Takes an ajax request and returns a splice
    """
    #get the review list
    if request.is_ajax:
        splice_count = int(request.GET.get('segment')) 
        beer = Beer.objects.get(id=request.GET.get('beer'))
        paginator = Paginator(Review.objects.order_by("date_created").filter(beer=beer.id), 4)
        p = paginator.page(splice_count)
        context = { 'review_list': p.object_list}
        return render_to_response('reviews/snippets/review_list_ajax.html', context)
        