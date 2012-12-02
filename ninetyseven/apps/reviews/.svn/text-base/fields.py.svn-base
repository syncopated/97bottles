from django import forms
from django.db.models import get_model
from django.utils import simplejson
from django.utils.safestring import mark_safe
from tagging.models import Tag

from savoy.contrib.sections.models import *

Review = get_model('reviews', 'review')

class AutoCompleteTagInput(forms.TextInput):
  def render(self, name, value, attrs=None):
    output = super(AutoCompleteTagInput, self).render(name, value, attrs)
    page_tags = [ section.slug for section in Section.objects.all() ]
    tag_list = simplejson.dumps([tag for tag in page_tags], ensure_ascii=False)
    return output + mark_safe(u'''
      <script type="text/javascript">
        if(typeof(jQuery) === "function"){
          $("#id_%s").autocomplete(%s, {
            width: 150,
            max: 10,
            highlight: false,
            multiple: true,
            multipleSeparator: ", ",
            scroll: true,
            scrollHeight: 300,
            matchContains: false,
            autoFill: true
          });
        }
      </script>
    ''' % (name, tag_list))