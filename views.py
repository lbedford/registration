from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.models import User

from registration.models import Event
from registration.models import UserRegistration
from registration.forms import LbwForm
from registration.forms import EventForm
from registration.forms import UserRegistrationForm

def index(request, old_form=None):
  lbws = Event.objects.filter(event_type=6).order_by('-start_date')
  form = LbwForm(instance=old_form)
  return render(
      request,
      'registration/index.html',
      {'lbws': lbws, 'form': form})

def detail(request, pk, old_form=None):
  event = get_object_or_404(Event, pk=pk)
  if event.event_type != 6:
    return HttpResponseRedirect(reverse('registration:index'))
  user_registration = None
  for ur in event.userregistration_set.all():
    if ur.user == request.user:
      user_registration = ur
  user_registration_form = UserRegistrationForm(instance=user_registration)
  event_form = EventForm(instance=old_form)
  return render(
      request,
      'registration/detail.html',
      {'event': event, 'event_form': event_form,
       'user_registration_form': user_registration_form})

def deregister(request, lbw_id):
  current_registration = get_object_or_404(UserRegistration, event_id=lbw_id, user_id=request.user.id)
  current_registration.delete()
  return HttpResponseRedirect(reverse('registration:index'))

def register(request, lbw_id):
    current_registration = UserRegistration.objects.all().filter(event_id=lbw_id, user_id=request.user.id)
    if current_registration:
      # update instead of create
      ur = current_registration[0]
    else:
      ur = UserRegistration(user_id=request.user.id, event_id=lbw_id)
    user_registration_form = UserRegistrationForm(request.POST, instance=ur)
    try:
      user_registration = user_registration_form.save()
      return HttpResponseRedirect(
          reverse('registration:detail', args=(user_registration.event_id,)))
    except ValueError:
      return detail(request, lbw_id, user_registration_form)

def propose(request):
    lbwForm = LbwForm(request.POST)
    try:
      return HttpResponseRedirect(
          reverse('registration:detail', args=(lbwForm.save().id,)))
    except ValueError:
      return index(request, lbwForm)

def activities(request, lbw_id):
    event = get_object_or_404(Event, pk=lbw_id)
    return render(request, 'registration/activities.html',
                  {'event': event})
   
def activity(request, lbw_id, activity_id):
    event = get_object_or_404(Event, pk=lbw_id)
    activity = get_object_or_404(Event, pk=activity_id)
    return render(request, 'registration/activity.html',
                  {'event': event, 'activity': activity})

def schedule(request, lbw_id):
    return HttpResponse("Showing schedule for lbw %s." % lbw_id)

def tshirts(request, lbw_id):
    return HttpResponse("Showing tshirts for lbw %s." % lbw_id)

def rides(request, lbw_id):
    return HttpResponse("Showing rides for lbw %s." % lbw_id)

def participants(request, lbw_id):
    return HttpResponse("Showing participants for lbw %s." % lbw_id)

def message(request, lbw_id, message_id):
    return HttpResponse("Viewing message for lbw %s, message %s." % (lbw_id, message_id))

def save_message(request, lbw_id):
    return HttpResponse("Saving message for lbw %s." % lbw_id)

def propose_activity(request, lbw_id):
    return HttpResponse("Proposing activity for lbw %s." % lbw_id)

def cancel_activity(request, lbw_id):
    return HttpResponse("Cancelling activity for lbw %s." % lbw_id)

def lbwuserview(request, lbw_id, user_id):
  lbw = get_object_or_404(Event, pk=lbw_id)
  return render(
      request,
      'registration/userview.html',
      {'lbw': lbw})
    
class UserView(generic.DetailView):
    model = User
    template_name = 'registration/userview.html'
