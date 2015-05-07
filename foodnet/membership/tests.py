# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from foodnet.membership.models import FoodnetUser


class TestFoodnetUserManager(TestCase):

    def test_create_user(self):
        user = get_user_model().objects.create_user(
            'test@food.net', is_active=True
        )
        self.assertIsInstance(user, FoodnetUser)
        self.assertEqual(1, get_user_model().objects.all().count())
        self.assertEqual(1, get_user_model().objects.all().count())

    def test_create_superuser(self):
        suser = get_user_model().objects.create_superuser(
            'test@food.net', email='test@food.net', password='pass'
        )
        self.assertIsInstance(suser, FoodnetUser)
        actual = get_user_model()\
            .objects.get(username='test@food.net')
        self.assertTrue(actual.is_superuser)


class TestMembership(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@food.net', is_active=True
        )
        self.user.set_password('pass')
        self.user.save()

    def test_profile(self):
        resp = self.client.get(reverse('profile'))
        url = reverse('log_in') + '?next=/membership/profile/'
        self.assertRedirects(resp, url, status_code=302,
                             target_status_code=200, msg_prefix='')

        self.client.login(username='test@food.net', password='pass')
        resp = self.client.get(reverse('profile'))
        self.assertContains(resp, 'profile', 2, 200)

    def test_log_out(self):
        self.client.login(username='test@food.net', password='pass')
        resp = self.client.get(reverse('log_out'), follow=True)
        url = reverse('home')
        self.assertRedirects(resp, url, status_code=302,
                             target_status_code=200, msg_prefix='')
        self.assertContains(resp, 'Log-in', 1, 200)
        self.assertNotContains(resp, 'Log-out')

    def test_user_profile_privacy(self):
        self.assertFalse(self.user.privacy)

    def test_log_in_get(self):
        resp = self.client.get(reverse('log_in'))
        self.assertContains(resp, 'Please log-in.', 2, 200)

    def test_log_in_invalid(self):
        resp = self.client.post(reverse('log_in'),
                                {'username': 'foo', 'password': 'bar'})
        self.assertContains(resp, 'Invalid email and/or password.', 1, 200)

    def test_log_in_incorect(self):
        resp = self.client.post(reverse('log_in'),
                                {'username': 'wrong-user@food.net',
                                 'password': 'some pass'})
        self.assertContains(resp, 'Incorrect email and/or password.', 1, 200)

    def test_log_in_inactive(self):
        self.user.is_active = False
        self.user.save()
        resp = self.client.post(reverse('log_in'),
                                {'username': 'test@food.net',
                                 'password': 'pass'})
        self.assertContains(resp, 'You email is no longer active.', 1, 200)

    def test_log_in_successfully(self):
        resp = self.client.post(reverse('log_in'),
                                {'username': 'test@food.net',
                                 'password': 'pass'}, follow=True)
        url = reverse('home')
        self.assertRedirects(resp, url, status_code=302,
                             target_status_code=200, msg_prefix='')
        self.assertContains(resp, 'You have successfully log-in.', 1, 200)

    def test_log_in_successfully_already(self):
        self.client.login(username='test@food.net', password='pass')
        resp = self.client.post(reverse('log_in'),
                                {'username': 'test@food.net',
                                 'password': 'pass'}, follow=True)
        url = reverse('home')
        self.assertRedirects(resp, url, status_code=302,
                             target_status_code=200, msg_prefix='')
        self.assertContains(resp, 'You are already logged-in.', 1, 200)
