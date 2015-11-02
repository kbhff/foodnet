from django.test import TestCase
from django.core.urlresolvers import reverse
from allauth.account.models import EmailAddress

from eggplant.profiles.models import UserProfile
from eggplant.factories import (
    UserFactory,
    AccountFactory,
    DepartmentFactory,
)


class TestPayments(TestCase):

    def setUp(self):
        self.test_user = UserFactory()
        self.assertTrue(UserProfile.objects.filter(user_id=self.test_user.id).exists())
        department = DepartmentFactory()
        self.user_profile = UserProfile.objects.filter(user_id=self.test_user.id).update(
            address=' test address',
            postcode='test postcode',
            city='test city',
            sex=UserProfile.FEMALE,
            tel='test tel',
        )
        AccountFactory.create(department=department, user_profiles=[self.user_profile])
        self.test_user.set_password('pass')
        self.test_user.save()
        email_address = EmailAddress.objects\
            .add_email(None, self.test_user, 'test@eggplant.dk', confirm=False,
                       signup=False)
        email_address.verified = True
        email_address.primary = True
        email_address.save()

        self.client.login(username=self.test_user.username, password='pass')

    def test_market_home(self):
        response = self.client.get(reverse('eggplant:market:market_home'))
        self.assertEqual(response.status_code, 200)

    def test_payment_accepted_nonexistent_order(self):
        non_existent = 1000000000000
        response = self.client.get(
            reverse('eggplant:market:payment_accepted', kwargs=dict(pk=non_existent)),
        )
        self.assertEqual(response.status_code, 404)

    def test_payment_rejected_nonexistent_order(self):
        non_existent = 1000000000000
        response = self.client.get(
            reverse('eggplant:market:payment_rejected',
                    kwargs=dict(pk=non_existent)))
        self.assertEqual(response.status_code, 404)
