from datetime import datetime
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Activity
from .models import Lbw


class LbwModelTest(TestCase):
    user = None

    def setUp(self):
        user = get_user_model()()
        user.save()
        first_name = "My"
        last_name = "Name"

    def test_cannot_create_lbw_with_no_settigs(self):
        lbw = Lbw()
        self.assertRaises(IntegrityError, lbw.save)

    def test_cannot_create_lbw_in_past(self):
        start_date = datetime.now() - timedelta(weeks=5)
        end_date = datetime.now() - timedelta(weeks=3)
        lbw = Lbw(start_date=start_date, end_date=end_date)
        self.assertRaises(ValidationError, lbw.clean)

    def test_cannot_create_lbw_that_ends_before_it_starts(self):
        start_date = datetime.now() + timedelta(weeks=5)
        end_date = datetime.now() + timedelta(weeks=3)
        lbw = Lbw(start_date=start_date, end_date=end_date)
        self.assertRaises(ValidationError, lbw.clean)

    def test_can_create_lbw(self):
        start_date = datetime.now() + timedelta(weeks=3)
        end_date = datetime.now() + timedelta(weeks=5)
        lbw = Lbw(start_date=start_date, end_date=end_date)
        lbw.clean()
        lbw.save()

    def test_schedule_days_with_no_events(self):
        start_date = datetime.now() + timedelta(weeks=3)
        end_date = datetime.now() + timedelta(weeks=4)
        lbw = Lbw(start_date=start_date, end_date=end_date)
        lbw.save()
        result = lbw.ScheduleDays()
        self.assertEqual(8, len(result), 'Incorrect number of scheduled days.')

    def test_schedule_days_with_events_before(self):
        start_date = datetime.now() + timedelta(weeks=3)
        end_date = datetime.now() + timedelta(weeks=4)
        lbw = Lbw(start_date=start_date, end_date=end_date)
        lbw.save()

        activity_start_date = datetime.now() + timedelta(weeks=2)
        activity = Activity(start_date=activity_start_date, duration=60)
        activity.save()

        lbw.activity.add(activity)
        lbw.save()

        result = lbw.ScheduleDays()

        self.assertEqual(9, len(result), 'Incorrect number of scheduled days')

    def test_schedule_days_with_events_after(self):
        start_date = datetime.now() + timedelta(weeks=3)
        end_date = datetime.now() + timedelta(weeks=4)
        lbw = Lbw(start_date=start_date, end_date=end_date)
        lbw.save()

        activity_start_date = datetime.now() + timedelta(weeks=5)
        activity = Activity(start_date=activity_start_date, duration=60)
        activity.save()

        lbw.activity.add(activity)
        lbw.save()

        result = lbw.ScheduleDays()

        self.assertEqual(9, len(result), 'Incorrect number of scheduled days')

    def test_schedule_days_with_events_before_and_after(self):
        start_date = datetime.now() + timedelta(weeks=3)
        end_date = datetime.now() + timedelta(weeks=4)
        lbw = Lbw(start_date=start_date, end_date=end_date)
        lbw.save()

        activity_start_date = datetime.now() + timedelta(weeks=5)
        activity = Activity(start_date=activity_start_date, duration=60)
        activity.save()

        lbw.activity.add(activity)

        activity_start_date = datetime.now() + timedelta(weeks=2)
        activity = Activity(start_date=activity_start_date, duration=60)
        activity.save()

        lbw.activity.add(activity)

        lbw.save()

        result = lbw.ScheduleDays()

        self.assertEqual(10, len(result), 'Incorrect number of scheduled days')

    def test_get_missing_users(self):
        pass

    def test_get_activities_per_day_by_time(self):
        pass

    def test_get_schedule(self):
        pass

    def test_unicode(self):
        start_date = datetime.now() + timedelta(weeks=3)
        end_date = datetime.now() + timedelta(weeks=4)
        lbw = Lbw(start_date=start_date, end_date=end_date, short_name='Ilkley Moor', description='bar tat')
        lbw.save()

        self.assertEqual('Ilkley Moor', lbw.__unicode__(), 'unicode method got broken')
        self.assertEqual('Ilkley Moor', lbw.__str__(), 'str method got broken')


