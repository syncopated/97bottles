from django import forms

from haystack.forms import *

def model_choices(site=None):
  from django.template.defaultfilters import capfirst
  if site is None:
    site = haystack.sites.site
  choices = [(m._meta, capfirst(unicode(m._meta.verbose_name_plural))) for m in site.get_indexed_models()]
  return sorted(choices, key=lambda x: x[1])


class SearchForm(ModelSearchForm):
  q = forms.CharField(required=False, label="Search for")

  def __init__(self, *args, **kwargs):
    super(SearchForm, self).__init__(*args, **kwargs)
    self.fields['models'] = forms.MultipleChoiceField(choices=model_choices(), required=False, widget=forms.CheckboxSelectMultiple, label="Limit results to")
  
  def search(self):
    sqs = super(ModelSearchForm, self).search()
    return sqs.models(*self.get_models())