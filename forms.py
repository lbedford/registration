"""Forms for LBW."""
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django import forms

from registration.models import Lbw
from registration.models import Accommodation
from registration.models import Activity
from registration.models import UserRegistration
from registration.models import Message


# pylint: disable=W0232
# pylint: disable=C1001
# pylint: disable=R0903

class LbwForm(forms.ModelForm):
  """LBW create/update form."""
  class Meta:
    """Meta."""
    model = Lbw
    exclude = ('attendees',)
    widgets = {
        'start_date': forms.TextInput(attrs={'class': 'datetimepicker'}),
        'end_date': forms.TextInput(attrs={'class': 'datetimepicker'}),
    }

  def __init__(self, *args, **kwargs):
    super(LbwForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_method = 'post'
    self.helper.add_input(Submit("submit", "Propose"))

class ActivityForm(forms.ModelForm):
  """Activity create/update form."""
  attachment = forms.FileField(required=False)
  
  class Meta:
    """Meta."""
    model = Activity
    fields = ('short_name', 'description', 'start_date',
              'duration', 'preferred_days', 'activity_type',
              'owners', 'attachment', 'attachment_type')
    widgets = {
        'start_date': forms.TextInput(attrs={'class': 'datetimepicker'}),
        }

  def __init__(self, *args, **kwargs):
    super(ActivityForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_method = 'post'

class UserRegistrationForm(forms.ModelForm):
  """LBW User registration form."""
  class Meta:
    """Meta."""
    model = UserRegistration
    exclude = ('user', 'lbw_user', 'lbw')
    widgets = {
        'arrival_date': forms.TextInput(attrs={'class': 'datetimepicker'}),
        'departure_date': forms.TextInput(attrs={'class': 'datetimepicker'}),
    }

  def __init__(self, *args, **kwargs):
    lbw = None
    if 'lbw' in kwargs:
      lbw = kwargs['lbw']
      del(kwargs['lbw'])
    super(UserRegistrationForm, self).__init__(*args, **kwargs)
    if lbw:
      self.fields['accommodation'].queryset = Accommodation.objects.filter(lbw=lbw)
    self.helper = FormHelper()
    self.helper.form_method = 'post'
    self.helper.form_class = 'form-horizontal'
    self.helper.label_class = 'col-sm-1 col-md-2'
    self.helper.field_class = 'col-sm-4'
    self.helper.add_input(Submit("submit", "Save"))
    self.helper.add_input(Submit("submit", "Deregister"))

class MessageForm(forms.ModelForm):
  """Message writing form."""
  class Meta:
    """Meta."""
    model = Message

  def __init__(self, *args, **kwargs):
    super(MessageForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_method = 'post'
    self.helper.add_input(Submit("submit", "Write"))

class AccommodationForm(forms.ModelForm):
  """Form to manage accommodation."""
  class Meta:
    """Meta."""
    exclude = ('lbw',)
    model = Accommodation

  def __init__(self, *args, **kwargs):
    super(AccommodationForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_method = 'post'
    self.helper.add_input(Submit("submit", "Add"))
