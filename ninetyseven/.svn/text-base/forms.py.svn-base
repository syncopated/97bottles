from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User

from savoy.core.new.profiles.models import *
from savoy.core.geo.models import *

class ProfileForm(ModelForm):
  display_name = forms.CharField(help_text="The name you want other 97bottles members to see")
  one_line_description = forms.CharField(label="One-line description", help_text="A little bit about you")
  avatar = forms.ImageField(label="Add a picture")
  class Meta:
    model = Profile
    exclude = ('user',)

ServiceFormSet  = inlineformset_factory(Profile, Service)
LinkFormSet     = inlineformset_factory(Profile, Link)

class UserForm(ModelForm):
  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'email')