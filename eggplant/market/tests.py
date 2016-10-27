from datetime import date
from decimal import Decimal

from allauth.account.models import EmailAddress
from django.core.urlresolvers import reverse
from django.test import TestCase
from eggplant.factories import AccountFactory, DepartmentFactory, UserFactory
from eggplant.market.models.cart import Basket
from eggplant.market.models.inventory import (Product, ProductCategory,
                                              ProductTax)
from eggplant.profiles.models import UserProfile


from moneyed import Money
from django.core.exceptions import ValidationError

class CommonSetUpPayments(TestCase):
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


class TestPayments(CommonSetUpPayments):

    def setUp(self):
        super(TestPayments, self).setUp()

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


class TestMarketModels(CommonSetUpPayments):

    def setUp(self):
        super(TestMarketModels, self).setUp()

        self.test_category = ProductCategory.objects.create(title='test_category')
        self.test_product_tax = ProductTax.objects.create(title='test_tax', tax=Decimal(0))

        self.test_product_1 = Product.objects.create(
            title='test_product_1',
            category=self.test_category,
            tax=self.test_product_tax,
            price=Money('20', 'DKK'))

        self.test_product_2 = Product.objects.create(
            title='test_product_2',
            category=self.test_category,
            tax=self.test_product_tax,
            price=Money('20', 'SEK'))

        self.test_basket = Basket.objects.create(
            user=self.test_user)

    def test_add_remove_products(self):

        self.assertEqual(self.test_basket.get_items_count(), 0)

        self.test_basket.add_to_items(product=self.test_product_1, quantity=2, delivery_date=None)
        self.assertEqual(self.test_basket.get_items_count(), 1)
        basket_items = self.test_basket.items.filter(product=self.test_product_1, delivery_date=None)

        self.assertEqual(basket_items[0].quantity, 2)

        # add the same product with the same delivery date => quantity is increased to 2+1
        self.test_basket.add_to_items(product=self.test_product_1, quantity=1, delivery_date=None)
        self.assertEqual(self.test_basket.get_items_count(), 1)

        basket_items = self.test_basket.items.filter(product=self.test_product_1, delivery_date=None)
        self.assertEqual(basket_items.count(), 1)
        self.assertEqual(basket_items[0].quantity, 3)

        # add the same product with a different delivery date
        # => 2 products in the basket

        self.test_basket.add_to_items(product=self.test_product_1, quantity=1, delivery_date=date.today())
        self.assertEqual(self.test_basket.get_items_count(), 2)

        basket_items = self.test_basket.items.filter(product=self.test_product_1, delivery_date=date.today())
        self.assertEqual(basket_items[0].quantity, 1)

        # remove product_1 with delivery date.today
        self.test_basket.remove_from_items(product=self.test_product_1, quantity=1, delivery_date=date.today())
        self.assertEqual(self.test_basket.get_items_count(), 1)

        # test if item are deleted
        basket_items = self.test_basket.items.filter(product=self.test_product_1, delivery_date=date.today())
        self.assertEqual(basket_items.count(), 0)

        # decrease quantity to 3-1 => 2
        self.test_basket.remove_from_items(product=self.test_product_1, quantity=1, delivery_date=None)
        basket_items = self.test_basket.items.filter(product=self.test_product_1, delivery_date=None)
        self.assertEqual(basket_items[0].quantity, 2)

    def test_backet_get_total_amount(self):
        self.assertEqual(self.test_basket.get_items_count(), 0)

        self.test_basket.add_to_items(product=self.test_product_1, quantity=2, delivery_date=None)

        total = self.test_basket.get_total_amount()

        self.assertEqual(total, Money(Decimal('40'), 'DKK'))

        with self.assertRaisesRegex(ValidationError, 'The products have different currencies'):
            self.test_basket.add_to_items(product=self.test_product_2, quantity=2, delivery_date=None)
            self.test_basket.get_total_amount()
