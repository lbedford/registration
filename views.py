"""Views for LBW."""
import datetime
import json

from crispy_forms.layout import Submit

from django.conf import settings
from django.core import serializers
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import StreamingHttpResponse, HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.timezone import UTC

from registration.models import Accommodation
from registration.models import Activity
from registration.models import Lbw
from registration.models import Message
from registration.models import UserRegistration
from registration.forms import ActivityForm
from registration.forms import AccommodationForm
from registration.forms import LbwForm
from registration.forms import MessageForm
from registration.forms import UserRegistrationForm

def get_basic_template_info(lbw_id=None):
  context = {}
  if lbw_id:
    context['lbw'] = get_object_or_404(Lbw, pk=lbw_id)
  context['lbws'] = Lbw.objects.order_by('-start_date')
  return context

def index(request):
  """Print out an index of the known LBWs."""
  context = get_basic_template_info()
  return render(request, 'registration/index.html', context)

def detail(request, lbw_id):
  """Print out a particular LBW."""
  context = get_basic_template_info(lbw_id)
  user_registration_form = None
  lbw_messages = None
  if request.user.is_authenticated():
    context['lbw_messages'] = Message.objects.filter(lbw_id=lbw_id).filter(activity=None)
  return render(request, 'registration/detail.html', context)

def deregister(request, lbw_id):
  """Deregister a user from an LBW."""

def register(request, lbw_id):
  """Register or update a registration for an LBW."""
  if not request.user.is_authenticated():
    return HttpResponseRedirect(reverse('registration:detail',
                                args=(lbw_id,)))
  context = get_basic_template_info(lbw_id)
  try:
    user_registration = UserRegistration.objects.get(
        user__exact=request.user,
        lbw_id__exact=lbw_id)
  except UserRegistration.DoesNotExist:
    user_registration = UserRegistration(lbw_id=lbw_id, user_id=request.user.id,
            arrival_date=context['lbw'].start_date,
            departure_date=context['lbw'].end_date)
  if request.method == 'POST':
    action = request.POST.get('submit')
    if action == "Deregister":
      if user_registration.id:
        user_registration.delete()
      return HttpResponseRedirect(reverse('registration:detail',
                                  args=(lbw_id,)))
    user_registration_form = UserRegistrationForm(request.POST,
                                                  instance=user_registration,
                                                  lbw=lbw_id)
    if user_registration_form.is_valid():
      user_registration_form.save()
      return HttpResponseRedirect(
          reverse('registration:detail', args=(lbw_id,)))
  else:
    user_registration_form = UserRegistrationForm(
        instance=user_registration, lbw=lbw_id)
  context['user_registration_form'] = user_registration_form
  return render(request, 'registration/register.html', context)

def activities(request, lbw_id):
  """Get all the activities for an LBW."""
  context = get_basic_template_info(lbw_id)
  return render(request, 'registration/activities.html', context)

def propose_activity(request, lbw_id):
  """Get all the activities for an LBW."""
  if not request.user.is_authenticated():
    return HttpResponseRedirect(reverse('registration:activities',
                                args=(lbw_id,)))
  context = get_basic_template_info(lbw_id)
  if request.method == 'POST':
    instance = Activity(lbw_id=lbw_id)
    activity_form = ActivityForm(request.POST, instance=instance)
    if activity_form.is_valid():
      act = activity_form.save()
      if not act.owners.count():
        act.owners.add(request.user.lbwuser)
      if 'attachment' in request.FILES:
        act.attachment = request.FILES['attachment']
      act.save()
      if settings.LBW_TO_EMAIL:
        message = render_to_string('registration/new_activity.html',
                                   {'lbw': context['lbw'], 'activity': act,
                                    'domain': request.get_host()})
        email = EmailMessage("New activity %s proposed for LBW %s" % (act.short_name,
                                                                      context['lbw'].short_name),
                             message, settings.LBW_FROM_EMAIL,
                             settings.LBW_TO_EMAIL,
                             headers = {'Reply-To': settings.LBW_TO_EMAIL[0]})
        email.send()
      return HttpResponseRedirect(reverse('registration:activities',
                                  args=(lbw_id,)))
  else:
    activity_form = ActivityForm()
  context['activity_form'] = activity_form
  activity_form.helper.add_input(Submit("submit", "Propose"))
  return render(request, 'registration/propose_activity.html', context)

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
        start_time = datetime.time(hour, min, tzinfo=None)
      else:
        start_time = datetime.time(0, 0, tzinfo=None)
      return datetime.datetime.combine(start_date, start_time)
  except KeyError:
    return None

def activity(request, lbw_id, activity_id):
  """Print details for one activity."""
  context = get_basic_template_info(lbw_id)
  act = context['activity'] = get_object_or_404(Activity, pk=activity_id)
  if context['lbw'].id != act.lbw_id:
    raise Http404
  if request.method == 'POST':
    act.start_date = get_date_from_schedule_post(request.POST)
    act.save()
    return HttpResponseRedirect(reverse('registration:activities',
                                        args=(lbw_id,)))
  return render(request, 'registration/activity.html', context)

def activity_register(request, lbw_id, activity_id):
  """Toggle a user registration for an activity."""
  activity = get_object_or_404(Activity, pk=activity_id)
  lbw = get_object_or_404(Lbw, pk=lbw_id)
  if lbw.id != activity.lbw_id:
      raise Http404
  if not request.user.is_authenticated():
    return HttpResponseRedirect(reverse('registration:activity',
                                args=(lbw_id, activity_id)))
  if request.user in activity.attendees.all():
    activity.attendees.remove(request.user)
  else:
    activity.attendees.add(request.user)
  activity.save()
  return HttpResponseRedirect(reverse('registration:activity',
                                      args=(lbw_id, activity_id)))

def schedule(request, lbw_id):
  """Print out a schedule for an LBW."""
  context = get_basic_template_info(lbw_id)
  return render(request, 'registration/schedule.html', context)

def tshirts(request, lbw_id):
  """Nothing."""
  return HttpResponse("Showing tshirts for lbw %s." % lbw_id)

def rides(request, lbw_id):
  """Nothing."""
  return HttpResponse("Showing rides for lbw %s." % lbw_id)

def participants(request, lbw_id):
  """Print out everyone going to an LBW."""
  if not request.user.is_authenticated():
    return HttpResponseRedirect(reverse('registration:detail',
                                args=(lbw_id,)))
  context = get_basic_template_info(lbw_id)
  return render(request, 'registration/participants.html', context)

def write_lbw_message(request, lbw_id):
  return write_message(request, lbw_id, None)

def write_activity_message(request, lbw_id, activity_id):
  return write_message(request, None, activity_id)

def write_message(request, lbw_id, activity_id=None):
  if not request.user.is_authenticated():
    return HttpResponseRedirect(reverse('registration:index'))
  context = get_basic_template_info(lbw_id)
  if activity_id:
    context['activity'] = get_object_or_404(Activity, pk=activity_id)
  if not lbw_id:
    context['lbw'] = context['activity'].lbw
  context['message_form'] = MessageForm()
  return render(request, 'registration/message_write.html', context)

def save_message(request, lbw_id):
  """Save a message."""
  if request.user.is_authenticated():
    if request.method == 'POST':
      base_message = Message(writer=request.user,
                             lbw_id=lbw_id,
                             activity_id=request.POST.get('activity_id', None))
      message_form = MessageForm(request.POST, instance=base_message)
      if message_form.is_valid():
        message = message_form.save()
        if message.activity_id:
          return HttpResponseRedirect(reverse('registration:activity',
                                              args=(lbw_id, message.activity_id)))
        return HttpResponseRedirect(reverse('registration:detail',
                                            args=(message.lbw_id,)))
      else:
        context = get_basic_template_info(lbw_id)
        activity_id = request.POST.get('activity_id', None)
        if activity_id:
          context['activity'] = get_object_or_404(Activity, pk=activity_id)
        context['message_form'] = message_form
        return render(request, 'registration/message_write.html', context)
  return HttpResponseRedirect(reverse('registration:index'))

def reply_message(request, lbw_id, message_id):
  if request.user.is_authenticated():
    context = get_basic_template_info(lbw_id)
    context['message'] = get_object_or_404(Message, pk=message_id)
    context['activity'] = context['message'].activity
    context['message_form'] = MessageForm()
    return render(request, 'registration/message_write.html', context)
  return HttpResponseRedirect(reverse('registration:index'))

def delete_message(request, lbw_id, message_id):
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
  context = get_basic_template_info()
  if request.method == 'POST':
    form = LbwForm(request.POST)
    if form.is_valid():
      lbw = form.save()
      if not lbw.owners.count():
        lbw.owners.add(request.user.lbwuser)
        lbw.save()
      if settings.LBW_TO_EMAIL:
          message = render_to_string('registration/new_lbw.html',
                                     {'lbw': lbw, 'domain': request.get_host()})
          email = EmailMessage('New LBW proposed: %s' % lbw.short_name,
                               message, settings.LBW_FROM_EMAIL,
                               settings.LBW_TO_EMAIL,
                               headers = {'Reply-To': settings.LBW_TO_EMAIL[0]})
          email.send()
      return HttpResponseRedirect(
          reverse('registration:detail', args=(lbw.id,)))
  else:
    form = LbwForm()
  context['form'] = form
  return render(request, 'registration/propose_lbw.html', context)

def delete_lbw(request, lbw_id):
  """Delete an LBW."""
  context = get_basic_template_info(lbw_id)
  lbw = context['lbw']
  if request.method == 'POST':
    form_lbw_id = request.POST['lbw_id']
    if request.user.lbwuser in lbw.owners.all():
      lbw.delete()
      return HttpResponseRedirect(
          reverse('registration:index'))
  else:
    lbw = get_object_or_404(Lbw, pk=lbw_id)
    if request.user.lbwuser in lbw.owners.all():
      return render(request, 'registration/delete_lbw.html', context)
    else:
      return HttpResponseRedirect(
          reverse('registration:index'))

def update_lbw(request, lbw_id):
  """Update an LBW."""
  context = get_basic_template_info(lbw_id)
  lbw = context['lbw']
  if request.user.lbwuser not in lbw.owners.all():
    return HttpResponseRedirect(
        reverse('registration:detail', args=(lbw.id,)))
  if request.method == 'POST':
    form = context['form'] = LbwForm(request.POST, instance=lbw)
    if form.is_valid():
      lbw = form.save()
      if not lbw.owners.count():
        lbw.owners.add(request.user.lbwuser)
        lbw.save()
      return HttpResponseRedirect(
          reverse('registration:detail', args=(lbw.id,)))
  else:
    context['form'] = LbwForm(instance=lbw)
  return render(request, 'registration/propose_lbw.html', context)

def update_activity(request, lbw_id, activity_id):
  context = get_basic_template_info(lbw_id)
  activity = context['activity'] = get_object_or_404(Activity, pk=activity_id)
  if context['lbw'].id != activity.lbw_id:
    raise Http404
  if request.method == 'POST':
    activity_form = context['activity_form'] = ActivityForm(
            request.POST, instance=activity)
    if activity_form.is_valid():
      act = activity_form.save()
      if not act.owners.count():
        act.owners.add(request.user.lbwuser)
      if 'attachment' in request.FILES:
        act.attachment = request.FILES['attachment']
      act.save()
      return HttpResponseRedirect(reverse('registration:activities',
                                  args=(lbw_id,)))
  else:
    activity_form = context['activity_form'] = ActivityForm(instance=activity)
  activity_form.helper.add_input(Submit("submit", "Update"))
  return render(request, 'registration/propose_activity.html', context)

def cancel_activity(request, lbw_id, activity_id):
  """Delete an activity."""
  if request.is_ajax():
    try:
      activity = get_object_or_404(Activity, pk=activity_id)
      if request.user.lbwuser in activity.owners.all():
        activity.delete()
        return HttpResponse('ok')
    except KeyError:
      return HttpResponse('incorrectly formatted request')
  else:
    raise Http404

def activity_attachment(request, lbw_id, activity_id):
  """Return the attachment for an activity."""
  activity = get_object_or_404(Activity, pk=activity_id)
  lbw = get_object_or_404(Lbw, pk=lbw_id)
  if lbw.id != activity.lbw_id:
    raise Http404
  if not activity.attachment:
    raise Http404
  return StreamingHttpResponse(activity.attachment.chunks())

def accommodation(request, lbw_id):
  context = get_basic_template_info(lbw_id)
  if request.method == 'POST':
    if request.user.is_authenticated():
      accommodation = Accommodation(lbw_id=lbw_id)
      context['accommodation_form'] = AccommodationForm(request.POST,
                                                        instance=accommodation)
      if context['accommodation_form'].is_valid():
        acc = context['accommodation_form'].save()
	acc.save()
  else:
    context['accommodation_form'] = AccommodationForm()
  return render(request, 'registration/accommodation.html', context)

def get_serializable_value(value):
  if type(value) == unicode:
    return value.encode('utf8')
  elif str(type(value)) == "<class 'django.contrib.auth.models.User'>":
    return (value.serializable_value('first_name').encode('utf8'),
            value.serializable_value('last_name').encode('utf8'))
  else:
    return str(value)

def details_json(request, lbw_id):
  if not request.user.is_authenticated():
    return HttpResponseRedirect(reverse('registration:detail',
                                args=(lbw_id,)))
  lbw = get_object_or_404(Lbw, pk=lbw_id)
  data = {}
  fields = ['description', 'end_date', 'short_name',
            'location', 'lbw_url', 'start_date']
  for field in fields:
    data[field] = get_serializable_value(lbw.serializable_value(field))

  data['attendees'] = []
  for attendee in lbw.attendees.all():
    data['attendees'].append(get_serializable_value(attendee))

  data['activities'] = []
  for activity in lbw.activity.all():
    activity_details = {
        'type': activity.get_activity_type_display().encode('utf-8')}
    fields = ['short_name', 'description', 'duration', 'start_date']
    for field in fields:
      activity_details[field] = get_serializable_value(activity.serializable_value(field))
    activity_details['attendees'] = []
    for attendee in activity.attendees.all():
      activity_details['attendees'].append(get_serializable_value(attendee))
    data['activities'].append(activity_details)
  
  return HttpResponse(json.dumps(data), content_type="application/json")
