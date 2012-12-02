from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User

from ninetyseven.apps.preferences.models import *

class UserPreferenceForm(ModelForm):
  class Meta:
    model = UserPreference
    exclude = ('user',)