from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User

from savoy.core.new.profiles.models import *
from savoy.core.geo.models import *

class ProfileForm(ModelForm):
  class Meta:
    model = Profile
    exclude = ('user',)

ServiceFormSet  = inlineformset_factory(Profile, Service)
LinkFormSet     = inlineformset_factory(Profile, Link)

class UserForm(ModelForm):
  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'email')
        
        
class CityForm(ModelForm):
  class Meta:
    model = City
    fields = ('city','state','province','country')