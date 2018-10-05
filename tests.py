from datetime import datetime
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model

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

    def test_cannot_create_lbw_without_owners(self):
        start_date = datetime.now() + timedelta(weeks=3)
        end_date = datetime.now() + timedelta(weeks=5)
        lbw = Lbw(start_date=start_date, end_date=end_date)
        self.assertRaises(ValidationError, lbw.clean)