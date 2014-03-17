from django import forms

from registration.models import Lbw
from registration.models import Activity
from registration.models import UserRegistration
from registration.models import Message

class LbwForm(forms.ModelForm):
  class Meta:
    model = Lbw
    exclude = ('attendees')
    widgets = {
        'start_date': forms.TextInput(attrs={'class': 'datepicker'}),
        'end_date': forms.TextInput(attrs={'class': 'datepicker'}),
    }

class ActivityForm(forms.ModelForm):
  class Meta:
    model = Activity
    fields = ('short_name', 'description', 'start_date',
              'duration', 'preferred_days', 'activity_type',
              'owners')

class UserRegistrationForm(forms.ModelForm):
  arrival_time = forms.CharField()
  departure_time = forms.CharField()
  class Meta:
    model = UserRegistration
    exclude = ('user', 'lbw')
    widgets = {
        'arrival_date': forms.TextInput(attrs={'class': 'datepicker'}),
        'departure_date': forms.TextInput(attrs={'class': 'datepicker'}),
    }

class MessageForm(forms.ModelForm):
  class Meta:
    model = Message

class LoginForm(forms.Form):
  username = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput())
