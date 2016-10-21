from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext_lazy as _

from eggplant.core.utils import disable_for_loaddata


class UserProfile(models.Model):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    SEX_CHOICES = (
        ('', '-----'),
        (FEMALE, 'female'),
        (MALE, 'male'),
        (OTHER, 'other'),
    )

    permissions = models.ManyToManyField(
        "permissions.Permission",
        verbose_name=_("permissions"),
        blank=True
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        editable=False,
        related_name='profile',
        verbose_name=_("user"),
    )
    middle_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name=_("middle name"),
        help_text=_("Optional.")
    )

    address = models.CharField(max_length=255)
    postcode = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    tel = models.CharField(max_length=15)
    tel2 = models.CharField(max_length=15, blank=True)
    sex = models.CharField(
        max_length=100,
        choices=SEX_CHOICES,
        blank=True
    )
    photo = models.ImageField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    changed = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return 'Profile({0})'.format(self.user)

    @property
    def full_name(self):
        """Returns member's full name."""
        if self.middle_name:
            names = [self.user.first_name,
                     self.middle_name,
                     self.user.last_name]
        else:
            names = [self.user.first_name, self.user.last_name]
        return ' '.join(names)

    def is_complete(self):
        return all([self.address, self.postcode, self.city, self.tel])

    def has_admin_permission(self, department):
        return self.administrator_for.filter(department=department).exists()

    def can_be_edited_by(self, user_profile):
        # can be edited by user_profile if the user_profile is an admin of
        # the self.member.department department
        for account in self.account_set.all():
            if user_profile.has_admin_permission(department=account.department):
                return True
        return False

    def active_accounts(self):
        """
        Returns the active accounts.
        """
        # TODO: Figure out what accounts are active based on memberships.
        return self.accounts.all()

    def photo_url_or_default(self):
        if self.photo:
            return self.photo.url
        else:
            return static('img/default-profile-photo.png')

    @classmethod
    def in_department(cls, department, only_active_accounts=True):
        """
        Returns the user profiles linked to the given department via:
        UserProfile -> Account -> DepartmentMembership -> Department
        """
        account_filter = {}
        if only_active_accounts:
            account_filter['active'] = True

        return UserProfile.objects.filter(
            accounts__in=department.accounts.filter(**account_filter)) \
            .order_by('user__last_name')


# TODO: This does not work with AUTH_USER_MODEL
# See: https://github.com/django/django/commit/fdb5c98d7ee54c7f89ec10b0203263f1f5b37510
@receiver(post_save, sender=User, dispatch_uid='membership-user-profile')
@disable_for_loaddata
def create_user_profile(sender, instance, created, **kwargs):
    """Every time a user is created, we automatically create a profile for
    the user."""
    if created:
        # Set the reverse instance.profile so the new profile is available
        # immediately
        instance.profile = UserProfile.objects.create(user=instance)
