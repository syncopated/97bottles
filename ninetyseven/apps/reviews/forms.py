from django.forms import ModelForm
from django.db import models
from django import forms

from tagging.forms import TagField

from ninetyseven.apps.reviews.fields import AutoCompleteTagInput

Review = models.get_model("reviews","review")

class ReviewForm(ModelForm):
  characteristics = TagField(widget=AutoCompleteTagInput(), required=False, help_text="Use tags such as `nutty','bitter', and `brown' to describe this beer. Separate tags with spaces or commas.")

  class Meta:
    model = Review
    fields = ('rating', 'comment', 'vessel', 'serving_type', 'city', 'characteristics')
    
  def clean_rating(self):
    data = self.cleaned_data['rating']
    if data not in range(1,98):
      raise forms.ValidationError("Only ratings from 1-97 are allowed.")
    return data