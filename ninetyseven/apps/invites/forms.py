from django.forms import ModelForm
from django.db import models
from django import forms
from django.contrib.auth.models import User

Invite = models.get_model("invites","invite")

class InviteForm(ModelForm):
  class Meta:
    model = Invite
    fields = ('email')