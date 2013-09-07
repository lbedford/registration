from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Event(models.Model):
    SIZES = (
      (1, 'Full fat'),
      (2, 'Mini'),
      (3, 'Micro'),
      (4, 'One man alone in a bar'))
    EVENT_TYPES = (
        (1, 'Workshop'),
        (2, 'Excursion'),
        (3, 'Lecture'),
        (4, 'Community Event'),
        (5, 'Hike'),
        (6, 'LBW'),
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
    size = models.IntegerField(choices=SIZES, default=1, blank=True, null=True)
    description = models.CharField(max_length=400)
    short_name = models.CharField(max_length=20, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    attendees = models.ManyToManyField(User, blank=True, related_name='lbw_attendees', through='UserRegistration')
    location = models.CharField(max_length=100, blank=True)
    owners = models.ManyToManyField(User, related_name='lbw_owners')
    preferred_days = models.IntegerField(choices=DAYS, blank=True, null=True)
    event_type = models.IntegerField(choices=EVENT_TYPES, default=6)
    event_url = models.CharField(max_length=400, blank=True)
    lbw = models.ForeignKey('self', blank=True, null=True, related_name='activity')

    def timedelta(self):
      return self.start_date - now()

    def finished(self):
      return now() > self.end_date

    def adults(self):
      return self.attendees.count()

    def children(self):
      return sum([
        a.children for a in self.userregistration_set.all()])

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
    event = models.ForeignKey(Event)
    kind = models.IntegerField(choices=ACC_TYPES)
    name = models.CharField(max_length=40)

    def __unicode__(self):
      return ' - '.join([self.get_kind_display(), self.name])

class UserRegistration(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    arrival_date = models.DateTimeField()
    departure_date = models.DateTimeField()
    accomodation = models.ForeignKey(Accomodation, blank=True, null=True)
    children = models.IntegerField(default=0)

    def __unicode__(self):
      return ' - '.join([self.event.description, str(self.user)])

class Message(models.Model):
    event = models.ForeignKey(Event)
    next = models.IntegerField(blank=True, null=True)
    previous = models.IntegerField(blank=True, null=True)
    message = models.CharField(max_length=400)
    subject = models.CharField(max_length=40)
    writer = models.ForeignKey(User)
    posted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
      return self.subject
    
class Ride(models.Model):
    ride_from = models.CharField(max_length=100)
    ride_to = models.CharField(max_length=100)
    offerer = models.ForeignKey(User, related_name='ride_offerer')
    requester = models.ForeignKey(User, related_name='ride_requester')
    notes = models.CharField(max_length=100)
    lbw = models.ForeignKey(Event)
    
class Tshirt(models.Model):
    name = models.CharField(max_length=10)
    picture = models.CharField(max_length=40)
    event = models.ForeignKey(Event)
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
