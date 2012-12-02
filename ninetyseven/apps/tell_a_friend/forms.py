from django import forms

class TellAFriendForm(forms.Form):
  recipient = forms.EmailField()