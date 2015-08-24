# coding: utf8
import uuid

from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
from allauth.account.models import EmailAddress

from eggplant.membership.models import (
    UserProfile,
    DepartmentInvitation,
)
from eggplant.membership.factories import (
    UserFactory,
    UserProfileFactory,
    AccountFactory,
    AccountCategoryFactory,
    AccountMembershipFactory,
    DepartmentFactory,
    DepartmentInvitationFactory,
)

from .models import Order


class TestPayments(TestCase):

    def setUp(self):
        self.test_user = UserFactory()
        # FIXME: mock Userprofile.is_complete to return True
        UserProfile.objects.filter(user_id=self.test_user.id).update(
            address=' test address',
            postcode='test postcode',
            city='test city',
            sex='f',
            tel='test tel',
            date_of_birth=timezone.now(),
            privacy=True,
            user=self.test_user
        )
        self.test_user.set_password('pass')
        self.test_user.save()
        email_address = EmailAddress.objects\
            .add_email(None, self.test_user, 'test@eggplant.dk', confirm=False,
                       signup=False)
        email_address.verified = True
        email_address.primary = True
        email_address.save()

        department = DepartmentFactory()
        account = AccountFactory(department=department)
        account.accountmembership_set\
            .create(user_profile=self.test_user.userprofile, role='owner')

        self.client.login(email='test@eggplant.dk', password='pass')

    def test_payments_home(self):
        response = self.client.get(reverse('eggplant:payments:payments_home'))
        self.assertEqual(response.status_code, 302)

    def test_payment_accepted_nonexistent_order(self):
        non_existent = uuid.uuid4()
        response = self.client.get(
            reverse('eggplant:payments:payment_accepted',
                    kwargs=dict(pk=non_existent)))
        self.assertEqual(response.status_code, 404)

    def test_payment_rejected_nonexistent_order(self):
        non_existent = uuid.uuid4()
        response = self.client.get(
            reverse('eggplant:payments:payment_rejected',
                    kwargs=dict(pk=non_existent)))
        self.assertEqual(response.status_code, 404)
