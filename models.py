import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Lbw(models.Model):
    SIZES = (
      (1, 'Full fat'),
      (2, 'Mini'),
      (3, 'Micro'),
      (4, 'One man alone in a bar'))

    size = models.IntegerField(choices=SIZES, default=1, blank=True, null=True)
    description = models.CharField(max_length=400)
    short_name = models.CharField(max_length=20, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
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

    def schedule_days(self):
      delta = self.end_date - self.start_date
      return [self.start_date.date() + datetime.timedelta(days=d) for d in xrange(0, delta.days)]

    def __unicode__(self):
      return self.description

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
    description = models.CharField(max_length=400)
    short_name = models.CharField(max_length=20, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(default=60)
    attendees = models.ManyToManyField(User, editable=False, blank=True, related_name='activity_attendees')
    owners = models.ManyToManyField(User, editable=False, related_name='activity_owners')
    preferred_days = models.IntegerField(choices=DAYS, blank=True, null=True)
    activity_type = models.IntegerField(choices=ACTIVITY_TYPES, default=6)
    lbw = models.ForeignKey(Lbw, editable=False, blank=True, null=True, related_name='activity')

    def end_date(self):
      if not self.start_date:
        return None
      return self.start_date + datetime.timedelta(minutes=self.duration)

    def can_be_scheduled(self):
      return self.activity_type != 1

    def schedule(self):
      if not self.can_be_scheduled:
        return 'Always'
      return self.start_date

    def __unicode__(self):
      return self.description

class Accomodation(models.Model):
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
    arrival_date = models.DateTimeField()
    departure_date = models.DateTimeField()
    accomodation = models.ForeignKey(Accomodation, blank=True, null=True)
    children = models.IntegerField(default=0)

class Message(models.Model):
    activity = models.ForeignKey(Activity, blank=True, null=True, editable=False)
    lbw = models.ForeignKey(Lbw, blank=True, null=True, editable=False)
    next = models.ForeignKey('self', blank=True, null=True, editable=False, related_name='next_message')
    previous = models.ForeignKey('self', blank=True, null=True, editable=False, related_name='previous_message')
    message = models.CharField(max_length=400)
    subject = models.CharField(max_length=40)
    writer = models.ForeignKey(User, editable=False)
    posted = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

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
