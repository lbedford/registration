from django.forms import ModelForm

from registration.models import Lbw
from registration.models import Activity
from registration.models import UserRegistration
from registration.models import Message

class LbwForm(ModelForm):
  class Meta:
    model = Lbw
    exclude = ('owners', 'attendees')

class ActivityForm(ModelForm):
  class Meta:
    model = Activity
    exclude = ('owners', 'attendees')

class UserRegistrationForm(ModelForm):
  class Meta:
    model = UserRegistration
    exclude = ('user', 'lbw')

class MessageForm(ModelForm):
  class Meta:
    model = Message
