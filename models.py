"""Models for LBW."""
import collections
import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import LbwUser


# pylint: disable=no-member
class Lbw(models.Model):
    """Model of an LBW."""
    MIN_SCHEDULE_TIME = 15

    SIZES = (
        (1, 'Full fat'),
        (2, 'Mini'),
        (3, 'Micro'),
        (4, 'One man alone in a bar'),
        (5, 'Kriek'))

    size = models.IntegerField(choices=SIZES, default=1, blank=True, null=True)
    description = models.TextField()
    short_name = models.CharField(max_length=1001)
    start_date = models.DateTimeField(help_text="Format: YYYY-MMM-DD HH:MM:SS")
    end_date = models.DateTimeField(help_text="Format: YYYY-MMM-DD HH:MM:SS")
    attendees = models.ManyToManyField(
        User, blank=True, related_name='lbw_attendees', through='UserRegistration')
    location = models.CharField(max_length=1001, blank=True)
    owners = models.ManyToManyField(
        LbwUser, blank=True, related_name='lbw_owners')
    lbw_url = models.CharField(max_length=1000, blank=True)

    def timedelta(self):
        """The different between now and the start of the LBW."""
        return self.start_date - timezone.now()

    def finished(self):
        """Has the LBW finished?"""
        return timezone.now() > self.end_date

    def adults(self):
        """How many adults?"""
        return self.attendees.count()

    def children(self):
        """How many children?"""
        return sum([
            a.children for a in self.userregistration_set.all()])

    def schedule_days(self):
        """The days of the schedule."""
        date_map = {}
        for activity in self.activity.filter(start_date__lt=self.start_date):
            date_map[activity.start_date.date()] = 1
        for activity in self.activity.filter(start_date__gt=self.end_date):
            date_map[activity.start_date.date()] = 1
        delta = self.end_date - self.start_date
        return [self.start_date.date() + datetime.timedelta(days=d)
                for d in range(0, delta.days + 1)] + list(date_map.keys())

    def schedule_hours(self):
        """Available hours in schedules."""
        return range(0, 24)

    def get_min_schedule_time(self):
        """Interval in minutes for scheduling."""
        return self.MIN_SCHEDULE_TIME

    def schedule_minutes(self):
        """Available minutes in scheduling."""
        return range(0, 60, self.MIN_SCHEDULE_TIME)

    def get_missing_users(self):
        """Find users who registered but won't be at the LBW."""
        users = []
        for user_registration in self.userregistration_set.all():
            if (user_registration.arrival_date > self.end_date or
                    user_registration.departure_date < self.start_date):
                users.append(user_registration.user)
        return users

    def get_activities_per_day_by_time(self, start_date):
        """Get activities bucketed by day and time."""
        end_date = start_date + datetime.timedelta(days=1)
        return_value = {'day': start_date, 'times': [],
                        'arrivals': 0, 'departures': 0, 'attendees': 0}
        activities_per_time = collections.defaultdict(list)
        for activity in self.activity.filter(start_date__range=(start_date, end_date)):
            # { 'time': '12:15', 'activities: [a, b, c] }
            activities_per_time['%02d:%02d' % (
                activity.start_date.hour, activity.start_date.minute)].append(activity)
        for hour in self.schedule_hours():
            for minute in self.schedule_minutes():
                this_time = '%02d:%02d' % (hour, minute)
                return_value['times'].append(
                    {'time': this_time, 'activities': activities_per_time[this_time]})
        return return_value

    def get_activities_per_day(self, start_date):
        """Get activities on one day."""
        end_date = start_date + datetime.timedelta(days=1)
        # activities_per_time = collections.defaultdict(list)
        return self.activity.filter(start_date__range=(start_date, end_date)).order_by('start_date')

    def get_schedule(self):
        """Get the overall schedule."""
        schedule = []
        for day in self.schedule_days():
            schedule.append({'day': day,
                             'activities': self.get_activities_per_day(day)})
        return schedule

    def get_activity_types(self):
        """Get the possible activity types."""
        types = {}
        for activity in self.activity.all():
            types.setdefault(activity.activity_type,
                             activity.get_activity_type_display())
        return types

    def __unicode__(self):
        return self.short_name


class Activity(models.Model):
    """Model of an activity."""
    class Meta:
        """Metadata."""
        ordering = ['start_date']

    ACTIVITY_TYPES = (
        (1, 'Workshop'),
        (2, 'Excursion'),
        (3, 'Lecture'),
        (4, 'Community Activity'),
        (5, 'Hike'),
        (6, 'Run'),
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
    description = models.TextField()
    short_name = models.CharField(max_length=1001, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(default=60, help_text='minutes')
    attendees = models.ManyToManyField(User, editable=False, blank=True,
                                       related_name='activity_attendees')
    owners = models.ManyToManyField(LbwUser, blank=True,
                                    related_name='activity_owners')
    preferred_days = models.IntegerField(choices=DAYS, blank=True, null=True)
    activity_type = models.IntegerField(choices=ACTIVITY_TYPES, default=1)
    lbw = models.ForeignKey(Lbw, editable=False, blank=True, null=True,
                            related_name='activity', on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='attachments/', null=True)
    attachment_type = models.IntegerField(choices=ATTACHMENT_TYPE, default=3)

    def end_date(self):
        """End time for the activity."""
        if self.start_date:
            return self.start_date + datetime.timedelta(minutes=self.duration)
        return None

    def can_be_scheduled(self):
        """Can this be scheduled?"""
        return True

    def schedule(self):
        """Schedule details for this activity."""
        if not self.can_be_scheduled:
            return 'Always'
        return self.start_date

    def get_duration_in_units(self):
        """Duration of activity in units of time."""
        return self.duration / self.lbw.get_min_schedule_tie()

    def user_can_attend(self, user):
        """Can user attend this activity?"""
        try:
            user_registration = UserRegistration.objects.get(user__exact=user,
                                                             lbw__exact=self.lbw)
        except UserRegistration.DoesNotExist:
            return False
        if self.start_date:
            if (user_registration.arrival_date > self.end_date() or
                    user_registration.departure_date < self.start_date):
                return False
        return True

    def get_missing_users(self):
        """Find attendees who will not be able to attend."""
        return [user
                for user in self.attendees.all()
                if not self.user_can_attend(user)]

    def day(self):
        """Day the activity is scheduled for."""
        if self.start_date:
            return self.start_date.date()
        return None

    def hour(self):
        """Hour the activity is scheduled for."""
        if self.start_date:
            return timezone.localtime(self.start_date).hour
        return None

    def minute(self):
        """Minute the activity is scheduled for."""
        if self.start_date:
            return timezone.localtime(self.start_date).minute
        return None

    def __unicode__(self):
        return self.short_name


class Accommodation(models.Model):
    """Model for accommodation."""
    ACC_TYPES = (
        (1, 'Hotel'),
        (2, 'Campsite'),
        (3, 'Field'),
        (4, 'Bed and Breakfast'),
        (5, 'Hotel Garni'),
        (6, 'Pension'),
        (7, 'Holiday Cottage'),
        (8, 'Youth Hostel'),
        (9, 'Bunkhouse'),
    )
    lbw = models.ForeignKey(Lbw, on_delete=models.CASCADE)
    kind = models.IntegerField(choices=ACC_TYPES)
    name = models.CharField(max_length=1001)

    def __unicode__(self):
        return ' - '.join([self.get_kind_display(), self.name])

    def __str__(self):
        return ' - '.join([self.get_kind_display(), self.name])


class UserRegistration(models.Model):
    """Model for user -> lbw registration."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lbw = models.ForeignKey(Lbw, on_delete=models.CASCADE)
    arrival_date = models.DateTimeField(
        help_text="Format: YYYY-MMM-DD HH:MM:SS")
    departure_date = models.DateTimeField(
        help_text="Format: YYYY-MMM-DD HH:MM:SS")
    accommodation = models.ForeignKey(Accommodation, blank=True, null=True,
                                      on_delete=models.CASCADE)
    children = models.IntegerField(default=0)


class Message(models.Model):
    """Model for message."""
    activity = models.ForeignKey(Activity, blank=True, null=True,
                                 editable=False, on_delete=models.CASCADE)
    lbw = models.ForeignKey(Lbw, blank=True, null=True, editable=False,
                            on_delete=models.CASCADE)
    next = models.ForeignKey('self', blank=True, null=True, editable=False,
                             related_name='next_message',
                             on_delete=models.CASCADE)
    previous = models.ForeignKey('self', blank=True, null=True, editable=False,
                                 related_name='previous_message',
                                 on_delete=models.CASCADE)
    message = models.TextField()
    subject = models.CharField(max_length=1001)
    writer = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)
    posted = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def message_lines(self):
        """Get the lines of the message."""
        return self.message.splitlines()

    def __unicode__(self):
        return self.subject


class Ride(models.Model):
    """Unused model for ride offer."""
    ride_from = models.CharField(max_length=1001)
    ride_to = models.CharField(max_length=1001)
    offerer = models.ForeignKey(User, related_name='ride_offerer',
                                on_delete=models.CASCADE)
    requester = models.ForeignKey(User, related_name='ride_requester',
                                  on_delete=models.CASCADE)
    notes = models.CharField(max_length=1001)
    lbw = models.ForeignKey(Lbw, on_delete=models.CASCADE)


class Tshirt(models.Model):
    """Unused model for tshirts."""
    name = models.CharField(max_length=1001)
    picture = models.CharField(max_length=401)
    lbw = models.ForeignKey(Lbw, on_delete=models.CASCADE)
    price = models.IntegerField()


class TshirtOrders(models.Model):
    """Unused model for tshirt orders."""
    SHIRT_SIZES = (
        ('M - S', 'Men - Small'),
        ('M - M', 'Men - Medium'),
        ('M - L', 'Men - Large'),
        ('M - XL', 'Men - Large'),
    )
    tshirt = models.ForeignKey(Tshirt, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    size = models.CharField(max_length=51, choices=SHIRT_SIZES)
