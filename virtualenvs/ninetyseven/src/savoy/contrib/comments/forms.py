from django import forms

from savoy.contrib.comments.models import Comment

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment