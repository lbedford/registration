from django.db import IntegrityError
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


from accounts.models import LbwUser
from registration.forms import LbwForm
from registration.models import Lbw

class LbwPropertyTests(TestCase):
    def setUp(self):
        self.user = get_user_model()()
        self.user.first_name = "My"
        self.user.last_name = "Name"
        self.user.save()
        self.lbwUser = LbwUser(user=self.user)
        self.lbwUser.save()

    def test_create_lbw_form_no_details(self):
        form = LbwForm()
        
    def test_open_propose_lbw(self):
        response = self.client.get(reverse('registration:propose_lbw'))
        self.assertEqual(response.status_code, 200)

    def test_propose_lbw(self):
        self.client.force_login(self.user)
        form = LbwForm({'size': "3",
            'description': "Test LBW",
            'short_name': "test",
            'start_date': "2010-01-01 08:00:00",
            'end_date': "2010-01-08 18:00:00",
            'owners': [self.lbwUser],
            'lbw_url': "https://testinglbw.com"})
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse('registration:propose_lbw'), form)
        self.assertEqual(response.status_code, 200)


class LbwMethodTests(TestCase):
    pass
