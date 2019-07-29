import datetime
from django.db import IntegrityError
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


from accounts.models import LbwUser
from registration.forms import ActivityForm
from registration.models import Lbw, Activity

class ActivityTests(TestCase):
    def setUp(self):
        self.user = get_user_model()()
        self.user.first_name = "My"
        self.user.last_name = "Name"
        self.user.save()
        self.lbwUser = LbwUser(user=self.user)
        self.lbwUser.save()
        self.lbw = Lbw(description="Test LBW",
                       short_name="test",
                       start_date=datetime.datetime.now() - datetime.timedelta(days=7),
                       end_date=datetime.datetime.now())
        self.lbw.save()
        self.lbw.owners.add(self.lbwUser)
        self.lbw.save()
        self.activity = Activity(description="another test activity",
                short_name="another test",
                activity_type=1,
                lbw=self.lbw)
        self.activity.save()
        self.activity.owners.add(self.lbwUser)
        self.activity.save()

    def list_activities(self):
        response = self.client.get(reverse('registration:activities', args=[self.lbw.id]))
        print(response.content)
        self.assertFalse('Undefined' in response.content)
        self.assertTrue('another test' in response.content)
        self.assertEqual(response.status_code, 200)

    def test_propose_activity(self):
        return
        self.client.force_login(self.user)
        form = ActivityForm({'activity_type': "1",
            'description': "Test Activity",
            'short_name': "test",
            'duration': 60,
            'owners': [self.lbwUser],
            'attachment': '1234',
            'attachment_type': 3,
            'lbw': self.lbw})
        result = form.is_valid()
        print(form.errors)
        self.assertTrue(result)
        response = self.client.post(reverse('registration:propose_activity',
            args=[self.lbw.id]), form)
        self.assertEqual(response.status_code, 200)

