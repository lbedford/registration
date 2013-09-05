from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Lbw(models.Model):
    SIZES = (
      (1, 'Full fat'),
      (2, 'Mini'),
      (3, 'Micro'),
      (4, 'One man alone in a bar'))
    size = models.IntegerField(choices=SIZES, default=1)
    description = models.CharField(max_length=400)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    attendees = models.ManyToManyField(User, blank=True, related_name='lbw_attendees')
    location = models.CharField(max_length=100)
    owner = models.ManyToManyField(User, related_name='lbw_owners')

    def timedelta(self):
      return now() - self.start_date

    def finished(self):
      return now() > self.end_date

    def adults(self):
      return len(self.attendees)

    def children(self):
      c = 0
      for a in self.attendees:
        c = c + a.children
      return c

    def __unicode__(self):
      return self.description

class Event(models.Model):
    EVENT_TYPES = (
        (1, 'Workshop'),
        (2, 'Excursion'),
        (3, 'Lecture'),
        (4, 'Community Event'),
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
    short_name = models.CharField(max_length=20)
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)
    attendees = models.ManyToManyField(User, blank=True)
    preferred_days = models.IntegerField(choices=DAYS, blank=True)
    lbw = models.ForeignKey(Lbw)
    event_type = models.IntegerField(choices=EVENT_TYPES, default=0, blank=True)

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

class UserRegistration(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Lbw)
    arrival_date = models.DateTimeField()
    departure_date = models.DateTimeField()
    accomodation = models.ForeignKey(Accomodation)
    children = models.IntegerField(default=0)

class Message(models.Model):
    event = models.ForeignKey(Event)
    next = models.IntegerField()
    previous = models.IntegerField()
    message = models.CharField(max_length=400)
    subject = models.CharField(max_length=40)
    writer = models.ForeignKey(User)
    posted = models.DateTimeField()
    
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
    event = models.ForeignKey(Lbw)
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




