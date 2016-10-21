# coding: utf8
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
import factory


class UserFactory(factory.DjangoModelFactory):

    username = factory.Sequence(lambda n: 'user%d@food.net' % n)

    class Meta:
        model = settings.AUTH_USER_MODEL

    @classmethod
    def _generate(cls, create, attrs):
        """Override the default _generate() to disable the post-save signal."""
        from eggplant.profiles.models import create_user_profile
        user = super(UserFactory, cls)._generate(create, attrs)
        post_save.connect(create_user_profile, get_user_model(),
                          dispatch_uid='membership-user-profile')
        return user


class UserProfileFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'profiles.UserProfile'

    user = factory.SubFactory('eggplant.factories.UserFactory',
                              userprofile=None)


class AccountFactory(factory.DjangoModelFactory):

    department = factory.SubFactory(
        'eggplant.factories.DepartmentFactory'
    )
    category = factory.SubFactory(
        'eggplant.factories.AccountCategoryFactory'
    )

    @factory.post_generation
    def user_profiles(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of UserProfile instances were passed in, use them
            for user_profile in extracted:
                self.user_profiles.add(user_profile)

    class Meta:
        model = 'accounts.Account'


class AccountCategoryFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'category%d' % n)

    class Meta:
        model = 'accounts.AccountCategory'


class DepartmentFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'departments.Department'


class DepartmentAdministratorFactory(factory.DjangoModelFactory):
    profile = factory.SubFactory('eggplant.factories.UserProfileFactory')
    department = factory.SubFactory('eggplant.factories.DepartmentFactory')

    class Meta:
        model = 'departments.DepartmentAdministrator'


class DepartmentInvitationFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'invitations.DepartmentInvitation'
