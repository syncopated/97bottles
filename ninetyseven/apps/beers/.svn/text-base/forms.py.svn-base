from django.forms import ModelForm
from django.db import models
from django import forms
from django.contrib.contenttypes.models import ContentType

from categorization.fields import CategoryModelChoiceField
from ninetyseven.apps.beers.fields import *

Beer = models.get_model("beers","beer")
Brewery = models.get_model("beers","brewery")
UserRecommendation = models.get_model("beers","userrecommendation")
City = models.get_model("geo","city")
Category = models.get_model("categorization","category")
User = models.get_model("auth", "user")
Relationship = models.get_model("relationships", "relationship")
Review = models.get_model("reviews", "review")
Fave = models.get_model("faves","fave")

class BeerForm(ModelForm):
  brewery = forms.ModelChoiceField(Brewery.objects.all(), widget=forms.HiddenInput(), required=False)
  variety = CategoryModelChoiceField(Category.objects.all(), help_text="The variety of beer, such as 'American Ale', or 'Lager'.")
  class Meta:
    model = Beer
    fields = ('name','variety','alcohol_by_volume','alcohol_by_weight','ibu','color','batch','description')
  
  def clean_ibu(self):
    data = self.cleaned_data['ibu']
    if data:
      if data not in range(1,101):
        raise forms.ValidationError("IBU must be an integer between 1 and 100.")
      return data

class EditBeerForm(ModelForm):
  variety = CategoryModelChoiceField(Category.objects.all(), help_text="The variety of beer, such as 'American Ale', or 'Lager'.")
  class Meta:
    model = Beer
    fields = ('name','brewery','variety','alcohol_by_volume','alcohol_by_weight','ibu','color','batch','description')

class BreweryForm(ModelForm):
  name = forms.CharField(required=False)
  city = forms.ModelChoiceField(City.objects.all(), widget=forms.HiddenInput(), required=False)
  class Meta:
    model = Brewery
    fields = ('name','type','url','city')

class EditBreweryForm(ModelForm):
  name = forms.CharField(required=False)
  class Meta:
    model = Brewery
    fields = ('name','type','url',)

class CityForm(ModelForm):
  class Meta:
    model = City
    fields = ('city','state','province','country')

class UserRecommendationForm(ModelForm):
  def __init__(self, user, beer, *args, **kwargs):
    super(UserRecommendationForm, self).__init__(*args, **kwargs)
    
    # Narrow the list of available users in the to_user field to just
    # friends who have not fave'd or reviewed this beer.
    followers_users_list = [ relationship.from_user for relationship in Relationship.objects.filter(to_user=user) ]
    friend_list = Relationship.objects.filter(from_user=user, to_user__in=followers_users_list)
    friend_id_list = [ relationship.to_user.id for relationship in friend_list ]
    friends = User.objects.filter(id__in=friend_id_list)
    beer_content_type = ContentType.objects.get_for_model(Beer)
    available_user_ids = []
    for this_user in friends:
      faves = Fave.objects.filter(user=this_user, content_type=beer_content_type, object_id=beer.id)
      reviews = Review.objects.filter(created_by=this_user, beer=beer)
      existing_recommendations = UserRecommendation.objects.filter(from_user=user, to_user=this_user, beer=beer)
      if not faves and not reviews and not existing_recommendations:
        available_user_ids.append(this_user.id)
    self.fields['to_user'].queryset = User.objects.filter(id__in=available_user_ids).order_by('profile__display_name', 'username')
  
  to_user = UserProfileNameChoiceField(User.objects.all())
  class Meta:
    model = UserRecommendation
    fields = ('to_user',)