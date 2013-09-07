from django.forms import ModelForm

from registration.models import Event
from registration.models import UserRegistration
from registration.models import Message

class LbwForm(ModelForm):
  class Meta:
    model = Event
    exclude = ('owners', 'attendees', 'preferred_days', 'event_type', 'lbw')

class EventForm(ModelForm):
  class Meta:
    model = Event
    exclude = ('owners', 'attendees')

class UserRegistrationForm(ModelForm):
  class Meta:
    model = UserRegistration
    exclude = ('user', 'lbw', 'event')

class MessageForm(ModelForm):
  class Meta:
    model = Message
    exclude = ('posted', 'writer', 'updated', 'next', 'previous', 'event')
