from django.forms import ModelForm
from django.contrib.auth.models import User

from savoy.core.profiles.models import Profile
from savoy.core.people.models import Person

class UserForm(ModelForm):
  class Meta:
    model   = User
    fields  = (
      'first_name',
      'last_name',
      'email',
    )

class ProfileForm(ModelForm):
  class Meta:
    model   = Profile
    fields  = (
      'display_name',
      'one_line_description',
      'bio',
      'display_on_map',
      'gender',
      'interests',
      'occupation',
      'birthdate',
      'mobile_carrier',
      'mobile_number',
      'zip_code',
    )
