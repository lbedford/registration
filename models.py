import collections
import datetime

from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Lbw(models.Model):
    MIN_SCHEDULE_TIME = 15

    SIZES = (
      (1, 'Full fat'),
      (2, 'Mini'),
      (3, 'Micro'),
      (4, 'One man alone in a bar'))

    size = models.IntegerField(choices=SIZES, default=1, blank=True, null=True)
    description = models.TextField(max_length=400)
    short_name = models.CharField(max_length=20)
    start_date = models.DateTimeField(help_text="Format: YYYY-MMM-DD HH:MM:SS")
    end_date = models.DateTimeField(help_text="Format: YYYY-MMM-DD HH:MM:SS")
    attendees = models.ManyToManyField(User, blank=True, related_name='lbw_attendees', through='UserRegistration')
    location = models.CharField(max_length=100, blank=True)
    owners = models.ManyToManyField(User, related_name='lbw_owners')
    lbw_url = models.CharField(max_length=400, blank=True)

    def timedelta(self):
      return self.start_date - now()

    def finished(self):
      return now() > self.end_date

    def adults(self):
      return self.attendees.count()

    def children(self):
      return sum([
        a.children for a in self.userregistration_set.all()])

    def ScheduleDays(self):
      delta = self.end_date - self.start_date
      return [self.start_date.date() + datetime.timedelta(days=d) for d in xrange(0, delta.days)]

    def ScheduleHours(self):
      return xrange(0, 23)

    def GetMinScheduleTime(self):
      return self.MIN_SCHEDULE_TIME

    def ScheduleMinutes(self):
      return xrange(0, 60, self.MIN_SCHEDULE_TIME)

    def GetMissingUsers(self):
      users = []
      for user_registration in self.userregistration_set.all():
        if (user_registration.arrival_date > self.end_date or
            user_registration.departure_date < self.start_date):
          users.append(user_registration.user)
      return users

    def GetActivitiesPerDayByTime(self, start_date):
      end_date = start_date + datetime.timedelta(days=1)
      return_value = {'day': start_date, 'times': [], 'arrivals': 0, 'departures': 0, 'attendees': 0}
      activities_per_time = collections.defaultdict(list)
      for activity in self.activity.filter(start_date__range=(start_date, end_date)):
        # { 'time': '12:15', 'activities: [a, b, c] }
        activities_per_time['%02d:%02d' % (activity.start_date.hour, activity.start_date.minute)].append(activity)
      for hour in self.ScheduleHours():
        for minute in self.ScheduleMinutes():
          this_time = '%02d:%02d' % (hour, minute)
          return_value['times'].append({'time': this_time, 'activities': activities_per_time[this_time]})
      return return_value

    def GetActivitiesPerDay(self, start_date):
      end_date = start_date + datetime.timedelta(days=1)
      activities_per_time = collections.defaultdict(list)
      return self.activity.filter(start_date__range=(start_date, end_date))

    def GetSchedule(self):
      schedule = []
      for day in self.ScheduleDays():
        schedule.append({'day': day,
                         'activities': self.GetActivitiesPerDay(day)})
      return schedule

    def __unicode__(self):
      return self.short_name

class Activity(models.Model):
    ACTIVITY_TYPES = (
        (1, 'Workshop'),
        (2, 'Excursion'),
        (3, 'Lecture'),
        (4, 'Community Activity'),
        (5, 'Hike'),
    )
    DAYS = (
        (1, 'Sunday'),
        (2, 'Monday'),
        (4, 'Tuesday'),
        (8, 'Wednesday'),
        (16, 'Thursday'),
        (32, 'Friday'),
        (64, 'Saturday'),
    )
    ATTACHMENT_TYPE = (
        (1, 'GPS Track'),
        (2, 'Image'),
        (3, 'Data'),
    )
    description = models.TextField(max_length=400)
    short_name = models.CharField(max_length=20, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(default=60, help_text='minutes')
    attendees = models.ManyToManyField(User, editable=False, blank=True, related_name='activity_attendees')
    owners = models.ManyToManyField(User, related_name='activity_owners')
    preferred_days = models.IntegerField(choices=DAYS, blank=True, null=True)
    activity_type = models.IntegerField(choices=ACTIVITY_TYPES, default=6)
    lbw = models.ForeignKey(Lbw, editable=False, blank=True, null=True, related_name='activity')
    attachment = models.FileField(upload_to='attachments/', null=True)
    attachment_type = models.IntegerField(choices=ATTACHMENT_TYPE, default=3)

    def end_date(self):
      if self.start_date:
        return self.start_date + datetime.timedelta(minutes=self.duration)
      return None

    def CanBeScheduled(self):
      return self.activity_type != 1

    def Schedule(self):
      if not self.CanBeScheduled:
        return 'Always'
      return self.start_date

    def GetDurationInUnits(self):
      return self.duration / self.lbw.GetMinScheduleTime()

    def UserCanAttend(self, user_registration):
      if self.start_date:
        if (user_registration.arrival_date > self.end_date() or
            user_registration.departure_date < self.start_date):
          return False
      return True

    def GetMissingUsers(self):
      return [user_registration.user 
              for user_registration in self.lbw.userregistration_set.all()
	      if not self.UserCanAttend(user_registration) ]

    def day(self):
      if self.start_date:
        return self.start_date.date()
      return None

    def hour(self):
      if self.start_date:
        return self.start_date.hour
      return None

    def minute(self):
      if self.start_date:
        return self.start_date.minute
      return None

    def __unicode__(self):
      return self.short_name

class Accommodation(models.Model):
    ACC_TYPES = (
      (1, 'Hotel'),
      (2, 'Campsite'),
      (3, 'Field'),
      (4, 'Bed and Breakfast'),
      (5, 'Hotel Garni'),
      (6, 'Pension'),
      (7, 'Holiday Cottage'),
    )
    lbw = models.ForeignKey(Lbw)
    kind = models.IntegerField(choices=ACC_TYPES)
    name = models.CharField(max_length=40)

    def __unicode__(self):
      return ' - '.join([self.get_kind_display(), self.name])

class UserRegistration(models.Model):
    user = models.ForeignKey(User)
    lbw = models.ForeignKey(Lbw)
    arrival_date = models.DateTimeField(help_text="Format: YYYY-MMM-DD HH:MM:SS")
    departure_date = models.DateTimeField(help_text="Format: YYYY-MMM-DD HH:MM:SS")
    accomodation = models.ForeignKey(Accommodation, blank=True, null=True)
    children = models.IntegerField(default=0)

class Message(models.Model):
    activity = models.ForeignKey(Activity, blank=True, null=True, editable=False)
    lbw = models.ForeignKey(Lbw, blank=True, null=True, editable=False)
    next = models.ForeignKey('self', blank=True, null=True, editable=False, related_name='next_message')
    previous = models.ForeignKey('self', blank=True, null=True, editable=False, related_name='previous_message')
    message = models.TextField(max_length=400)
    subject = models.CharField(max_length=40)
    writer = models.ForeignKey(User, editable=False)
    posted = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def message_lines(self):
      return self.message.splitlines()

    def __unicode__(self):
      return self.subject
    
class Ride(models.Model):
    ride_from = models.CharField(max_length=100)
    ride_to = models.CharField(max_length=100)
    offerer = models.ForeignKey(User, related_name='ride_offerer')
    requester = models.ForeignKey(User, related_name='ride_requester')
    notes = models.CharField(max_length=100)
    lbw = models.ForeignKey(Lbw)
    
class Tshirt(models.Model):
    name = models.CharField(max_length=10)
    picture = models.CharField(max_length=40)
    lbw = models.ForeignKey(Lbw)
    price = models.IntegerField()
    
class TshirtOrders(models.Model):
    SHIRT_SIZES = (
        ('M - S', 'Men - Small'),
        ('M - M', 'Men - Medium'),
        ('M - L', 'Men - Large'),
        ('M - XL', 'Men - Large'),
    )
    tshirt = models.ForeignKey(Tshirt)
    user = models.ForeignKey(User)
    quantity = models.IntegerField()
    size = models.CharField(max_length=7, choices=SHIRT_SIZES)
