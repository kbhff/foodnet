# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase


class TestDashboard(TestCase):

    def test_home(self):
        response = self.client.get(reverse('eggplant:dashboard:home'))
        self.assertEqual(response.status_code, 302)
