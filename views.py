"""Views for LBW."""
import datetime

from django.core.urlresolvers import reverse
from django.http import StreamingHttpResponse, HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import UTC

from registration.models import Activity
from registration.models import Lbw
from registration.models import Message
from registration.models import UserRegistration
from registration.forms import ActivityForm
from registration.forms import DeleteLbwForm
from registration.forms import LbwForm
from registration.forms import MessageForm
from registration.forms import UserRegistrationForm

def index(request):
  """Print out an index of the known LBWs."""
  if request.user.is_authenticated():
    no_owning = Lbw.objects.exclude(owners__in=[request.user])
    no_attending = no_owning.exclude(attendees__in=[request.user])
    lbws = no_attending.order_by('-start_date')
  else:
    lbws = Lbw.objects.order_by('-start_date')
  return render(
      request,
      'registration/index.html',
      {'lbws': lbws})

def detail(request, lbw_id, old_form=None):
  """Print out a particular LBW."""
  lbw = get_object_or_404(Lbw, pk=lbw_id)
  user_registration_form = None
  lbw_messages = None
  if request.user.is_authenticated():
    if old_form:
      user_registration_form = old_form
    else:
      try:
        user_registration = UserRegistration.objects.get(
            user__exact=request.user,
            lbw__exact=lbw)
        user_registration_form = UserRegistrationForm(
            instance=user_registration)
      except UserRegistration.DoesNotExist:
        user_registration_form = UserRegistrationForm(
            initial={'arrival_date': lbw.start_date,
                     'departure_date': lbw.end_date})
    lbw_messages = Message.objects.filter(lbw=lbw).filter(activity=None)
  return render(
      request,
      'registration/detail.html',
      {'lbw': lbw,
       'lbw_messages': lbw_messages,
       'user_registration_form': user_registration_form})

def deregister(request, lbw_id):
  """Deregister a user from an LBW."""
  current_registration = get_object_or_404(
      UserRegistration, lbw_id=lbw_id, user=request.user)
  current_registration.delete()
  return HttpResponseRedirect(reverse('registration:detail',
                              args=(lbw_id,)))

def register(request, lbw_id):
  """Register or update a registration for an LBW."""
  current_registration = UserRegistration.objects.all().filter(
      lbw_id=lbw_id, user=request.user)
  if current_registration:
    # update instead of create
    registration = current_registration[0]
  else:
    registration = UserRegistration(lbw_id=lbw_id, user=request.user)
  user_registration_form = UserRegistrationForm(request.POST,
                                                instance=registration)
  try:
    user_registration_form.save()
    return HttpResponseRedirect(
        reverse('registration:detail', args=(lbw_id,)))
  except ValueError:
    return detail(request, lbw_id, user_registration_form)

def activities(request, lbw_id):
  """Get all the activities for an LBW."""
  lbw = get_object_or_404(Lbw, pk=lbw_id)
  if request.method == 'POST':
    instance = None
    if 'activity_id' in request.POST:
      instance = get_object_or_404(Activity, pk=request.POST['activity_id'])
    activity_form = ActivityForm(request.POST, instance=instance)
    if activity_form.is_valid():
      act = activity_form.save()
      if not instance:
        act.lbw = lbw
        if request.user not in act.owners.all():
          act.owners.add(request.user)
      if 'attachment' in request.FILES:
        act.attachment = request.FILES['attachment']
      act.save()
    else:
      print 'activity_form is not valid'
  else:
    activity_form = ActivityForm()
  return render(request, 'registration/activities.html',
                {'lbw': lbw, 'activity_form': activity_form})

def get_date_from_schedule_post(schedule_post):
  """Parse POST data to find a date."""
  try:
    if schedule_post['activity_day']:
      (month, day, year) = schedule_post['activity_day'].split('/')
      start_date = datetime.date(int(year), int(month), int(day))
      if schedule_post['activity_hour']:
        hour = int(schedule_post['activity_hour'])
        min = 0
        if schedule_post['activity_min']:
          min = int(schedule_post['activity_min'])
        start_time = datetime.time(hour, min, tzinfo=UTC())
      else:
        start_time = datetime.time(0, 0, tzinfo=UTC())
      return datetime.datetime.combine(start_date, start_time)
  except KeyError:
    return None

def activity(request, activity_id):
  """Print details for one activity."""
  act = get_object_or_404(Activity, pk=activity_id)
  lbw_id = act.lbw_id
  if request.method == 'POST':
    act.start_date = get_date_from_schedule_post(request.POST)
    act.save()
    return HttpResponseRedirect(reverse('registration:activities',
                                        args=(lbw_id,)))
  else:
    activity_form = ActivityForm(instance=act)
  return render(request, 'registration/activity.html',
                {'lbw': act.lbw, 'activity': act,
                'activity_form': activity_form})

def activity_register(request, lbw_id, activity_id):
  """Toggle a user registration for an activity."""
  act = get_object_or_404(Activity, pk=activity_id)
  if request.user in act.attendees.all():
    act.attendees.remove(request.user)
  else:
    act.attendees.add(request.user)
  act.save()
  return HttpResponseRedirect(reverse('registration:activity',
                                      args=(lbw_id, activity_id)))

def schedule(request, lbw_id):
  """Print out a schedule for an LBW."""
  lbw = get_object_or_404(Lbw, pk=lbw_id)
  return render(
      request,
      'registration/schedule.html',
      {'lbw': lbw})

def tshirts(request, lbw_id):
  """Nothing."""
  return HttpResponse("Showing tshirts for lbw %s." % lbw_id)

def rides(request, lbw_id):
  """Nothing."""
  return HttpResponse("Showing rides for lbw %s." % lbw_id)

def participants(request, lbw_id):
  """Print out everyone going to an LBW."""
  lbw = get_object_or_404(Lbw, pk=lbw_id)
  return render(
      request,
      'registration/participants.html',
      {'lbw': lbw, 'users': lbw.userregistration_set.all()})

def message(request, lbw_id, message_id):
  """Read a message."""
  if not request.user.is_authenticated():
    return HttpResponseRedirect(reverse('registration:index'))
  lbw = get_object_or_404(Lbw, pk=lbw_id)
  my_message = get_object_or_404(Message, pk=message_id)
  return render(request, 'registration/message.html',
                {'lbw': lbw, 'message': my_message})

def write_lbw_message(request, lbw_id):
  return write_message(request, lbw_id, None)

def write_activity_message(request, activity_id):
  return write_message(request, None, activity_id)

def write_message(request, lbw_id, activity_id=None):
  if not request.user.is_authenticated():
    return HttpResponseRedirect(reverse('registration:index'))
  activity = None
  if activity_id:
    activity = get_object_or_404(Activity, pk=activity_id)
  if lbw_id:
    lbw = get_object_or_404(Lbw, pk=lbw_id)
  else:
    lbw = activity.lbw
  message_form = MessageForm()
  return render(request, 'registration/message_write.html',
                {'lbw': lbw, 'activity': activity,
                 'message_form': message_form})

def save_message(request):
  """Save a message."""
  if request.user.is_authenticated():
    if request.method == 'POST':
      base_message = Message(writer=request.user,
                             lbw_id=request.POST.get('lbw_id'),
                             activity_id=request.POST.get('activity_id', None))
      message_form = MessageForm(request.POST, instance=base_message)
      message = message_form.save()
      if message.activity_id:
        return HttpResponseRedirect(reverse('registration:activity',
                                            args=(message.activity_id,)))
      return HttpResponseRedirect(reverse('registration:detail',
                                          args=(message.lbw_id,)))
  return HttpResponseRedirect(reverse('registration:index'))

def delete_message(request, message_id):
  """Delete a message."""
  if request.is_ajax():
    try:
      message = get_object_or_404(Message, pk=message_id)
      if request.user == message.writer:
        message.delete()
        return HttpResponse('ok')
    except KeyError:
      return HttpResponse('incorrectly formatted request')
  else:
    raise Http404

def propose_lbw(request):
  """Propose an LBW."""
  if request.method == 'POST':
    form = LbwForm(request.POST)
    if form.is_valid():
      lbw = form.save()
      lbw.owners.add(request.user)
      lbw.save()
      return HttpResponseRedirect(
          reverse('registration:detail', args=(lbw.id,)))
  else:
    form = LbwForm()
  return render(
      request,
      'registration/propose_lbw.html',
      {'form': form})

def delete_lbw(request, lbw_id):
  """Delete an LBW."""
  if request.method == 'POST':
    form_lbw_id = request.POST['lbw_id']
    lbw = get_object_or_404(Lbw, pk=form_lbw_id)
    if request.user in lbw.owners.all():
      form = DeleteLbwForm(request.POST, instance=lbw)
      if form.is_valid():
        lbw.delete()
        return HttpResponseRedirect(
            reverse('registration:index'))
  else:
    lbw = get_object_or_404(Lbw, pk=lbw_id)
    if request.user in lbw.owners.all():
      form = DeleteLbwForm(instance=lbw)
      return render(
        request, 'registration/delete_lbw.html',
        {'form': form})
    else:
      return HttpResponseRedirect(
          reverse('registration:index'))

def update_lbw(request, lbw_id):
  """Update an LBW."""
  if request.method == 'POST':
    form_lbw_id = request.POST['lbw_id']
    lbw = get_object_or_404(Lbw, pk=form_lbw_id)
    if request.user in lbw.owners.all():
      form = LbwForm(request.POST, instance=lbw)
      if form.is_valid():
        form.save()
        return HttpResponseRedirect(
            reverse('registration:detail', args=(lbw.id,)))
    else:
      return HttpResponseRedirect(
          reverse('registration:detail', args=(lbw.id,)))
  else:
    lbw = get_object_or_404(Lbw, pk=lbw_id)
    if request.user not in lbw.owners.all():
      return HttpResponseRedirect(
          reverse('registration:detail', args=(lbw.id,)))

    form = LbwForm(instance=lbw)
  return render(
      request, 'registration/propose_lbw.html',
      {'form': form})

def cancel_activity(request, activity_id):
  """Delete an activity."""
  if request.is_ajax():
    try:
      activity = get_object_or_404(Activity, pk=activity_id)
      if request.user in activity.owners.all():
        activity.delete()
        return HttpResponse('ok')
    except KeyError:
      return HttpResponse('incorrectly formatted request')
  else:
    raise Http404

def activity_attachment(request, activity_id):
  """Return the attachment for an activity."""
  activity = get_object_or_404(Activity, pk=activity_id)
  if not activity.attachment:
    raise Http404
  return StreamingHttpResponse(activity.attachment.chunks())
