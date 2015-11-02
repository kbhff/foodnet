import os

from django.conf import settings
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
from eggplant.accounts.models import Account

from eggplant.core.utils import absolute_url_reverse
from eggplant.factories import UserFactory, DepartmentFactory, \
    AccountCategoryFactory, DepartmentInvitationFactory
from eggplant.profiles.models import UserProfile

from .models import DepartmentInvitation


class TestInvite(TestCase):

    def setUp(self):
        self.user = UserFactory(email='test_admin@food.net')
        self.user.set_password('pass')
        self.user.is_superuser = True

        self.department = DepartmentFactory()
        self.account_category = AccountCategoryFactory()

        content_type = ContentType.objects.get_for_model(DepartmentInvitation)
        can_invite = Permission.objects.get(content_type=content_type,
                                            codename='can_invite')
        self.user.user_permissions.add(can_invite)
        self.user.save()
        os.environ['RECAPTCHA_TESTING'] = 'True'

    def test_get(self):
        self.client.login(username=self.user.username, password='pass')
        response = self.client.get(reverse('eggplant:invitations:invite'))
        self.assertTemplateUsed(response, 'eggplant/invitations/invite.html')

    def test_user_already_verified(self):
        data = {
            'department': self.department.id,
            'email': self.user.email,
            'account_category': self.account_category.id,
        }
        self.client.login(username=self.user.email, password='pass')
        response = self.client.post(reverse('eggplant:invitations:invite'),
                                    data=data, follow=True)
        expected = 'User {} already exists'.format(self.user.email)
        self.assertContains(response, expected, 1, 200)

    def test_send_invitation(self):
        invited_email = 'test1@localhost'
        data = {
            'department': self.department.id,
            'email': invited_email,
            'account_category': self.account_category.id,
        }
        self.client.login(username=self.user.username, password='pass')
        response = self.client.post(reverse('eggplant:invitations:invite'),
                                    data=data, follow=True)

        self.assertRedirects(response, reverse('eggplant:dashboard:home'))

        expected = 'Invitation has been send to {}'.format(invited_email)
        self.assertContains(response, expected, 1, 200)

        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(bool(mail.outbox[0].subject))

        invitation = DepartmentInvitation.objects.get(email=invited_email)

        url = absolute_url_reverse(
            'eggplant:invitations:accept_invitation',
            kwargs=dict(verification_key=invitation.verification_key.hex)
        )
        self.assertRegex(invitation.verification_key.hex, r'^[a-z0-9]{32}\Z')
        self.assertIn(url, mail.outbox[0].body)

    def test_accept_invitation_flow(self):
        invited_email = 'test2@food.net'
        invitation = DepartmentInvitationFactory(
            email=invited_email,
            invited_by=self.user,
            department=self.department,
            account_category=self.account_category,
        )
        accept_invitation_url = reverse(
            'eggplant:invitations:accept_invitation',
            kwargs=dict(verification_key=invitation.verification_key.hex)
        )

        if settings.USE_RECAPTCHA:
            response = self.client.get(accept_invitation_url)
            self.assertContains(response, 'accept invitation', 2)
            self.assertContains(response, invitation.verification_key.hex, 1)

            data = {
                'recaptcha_responseonse_field': 'PASSED',
            }
            response = self.client.post(
                accept_invitation_url,
                data=data,
                follow=True
            )
            url_name = 'account_set_password'
            self.assertRedirects(response, reverse(url_name),
                                 status_code=302,
                                 target_status_code=200,
                                 msg_prefix='',)
        else:
            response = self.client.get(accept_invitation_url, follow=True)
            self.assertRedirects(
                response,
                reverse('account_set_password'),
                status_code=302,
                target_status_code=200
            )
        self.assertContains(response, 'password1', 3)
        self.assertContains(response, 'password2', 3)

        # test for creating default account for new user
        actual = Account.objects.all().count()
        self.assertEqual(1, actual)
        actual = Account.objects.all()[0]
        test_user = User.objects.get(email=invited_email)
        self.assertEqual(actual.user_profiles.all()[0], test_user.profile)

        data = {
            'password1': 'passpass123',
            'password2': 'passpass123',
        }
        response = self.client.post(
            reverse('account_set_password'),
            data=data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('account_login') + '?next=' + reverse('eggplant:profiles:profile'),
            status_code=302,
            target_status_code=200
        )

        data = {
            'login': invited_email,
            'password': 'passpass123',
        }
        response = self.client.post(
            reverse('account_login'),
            data=data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('eggplant:profiles:profile'),
            status_code=302,
            target_status_code=200
        )

        # check if a new user is forced to complete it's profile
        response = self.client.get(reverse('eggplant:dashboard:home'),
                                   follow=True)
        self.assertRedirects(
            response,
            reverse('eggplant:profiles:profile'),
            status_code=302,
            target_status_code=200
        )
        expected = 'Please update your profile.'
        actual = [m.message for m in list(response.context['messages'])]
        self.assertIn(expected, actual)

        data = {
            'first_name': 'first_name',
            'middle_name': '',
            'last_name': 'last_name',
            'address': 'Vestergade 20C',
            'city': 'Copenhagen',
            'postcode': '123321',
            'tel': '231321321',
            'sex': UserProfile.FEMALE,
        }
        response = self.client.post(reverse('eggplant:profiles:profile'),
                                    data=data, follow=True)
        self.assertRedirects(
            response,
            reverse('eggplant:dashboard:home'),
            status_code=302,
            target_status_code=200
        )
        expected = 'Your profile has been successfully updated.'
        actual = [m.message for m in list(response.context['messages'])]
        self.assertIn(expected, actual)
        self.assertContains(response, 'Log out', 1)

    def test_change_password_get(self):
        self.client.login(username=self.user.username, password='pass')
        response = self.client.get(reverse('account_change_password'))
        self.assertTemplateUsed(response, 'account/password_change.html')
        self.assertContains(response, 'Change Password')
