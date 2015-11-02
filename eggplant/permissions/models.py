"""
Permission philosophy:

    - Be explicit!
      Uses boolean fields for specific tasks
    - Be SQL friendly, create permissions that are nice to work with in
      query set lookups
    - Put logic in decorators

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserProfilePermission(models.Model):
    """
    Link between a user profile and a set of permissions (a role).

    Example 1:
    Check if a user has user creation access to a department:

    can_add_users = department.userprofilepermission_set.filter(
        user_profile__user=request.user,
        permission__can_add_user_profiles=True
    ).exists()

    if can_add_users:
        obama_speech = "YES WE CAN"
        print(obama_speech)


    Example 2:
    Check if user can manage an account, like changing the data:

    can_change_account = account.userprofilepermission_set.filter(
        user_profile__user=request.user,
        permission__can_change_accounts=True,
    )

    if not can_change_account:
        return HttpNotAllowed("piss off")


    TODO: Create decorators to manage this easier!

    """
    user_profile = models.ForeignKey('profiles.UserProfile')
    permission = models.ForeignKey('permissions.Permission')

    is_global = models.BooleanField(
        _("global"),
        help_text=_("This permission gives access across all departments"),
        default=False
    )

    department = models.ForeignKey(
        'departments.Department'
    )
    account = models.ForeignKey(
        'accounts.Account'
    )


class Permission(models.Model):
    """
    Permission roles are a set of permissions. Permissions are modeled as
    booleans in this model.

    What can a user do? Examples from discussion of different roles:

    A user is a superuser:
        Don't put it here -- THIS IS FOR THE global User.is_superuser field!!

    A user can create and manage all departments.:
        E.g. someone from the central commission can add a new department and
        close an existing one.

    A user is a department manager:
        Can create and delete accounts and user profiles for everyone in a
        department.

    A user is an "intro vagt":
        Someone who can create new accounts

    A user is a team link:
        Can manage volunteer shifts

    A user owns an account:
        Can add credit card, can add others to the account


    CONCEPT OF THIS MODEL: Create boolean fields for different permissions,
    create lots of them! We want to be very explicit.
    """

    name = models.CharField(
        verbose_name=_("name"),
        max_length=64,
        help_text=_(
            "Human readable name, not used for any lookups so can be anything"
        ),
    )

    # NEVER USE THIS IN A LOOKUP! USE EXPLICIT FIELDS
    all_permissions = models.BooleanField(
        _("all permissions"),
        default=False,
        help_text=_("Grant all permissions")
    )

    can_add_user_profiles = models.BooleanField(
        _("add users"),
        default=False,
        help_text=_(
            "Can add users to associated account or department, meaning that "
            "setting this value is only meaningful if an account or department "
            "is associated."
        ),
    )

    can_change_account = models.BooleanField(
        _("change account(s)"),
        default=False,
        help_text=_(
            "Can change associated accounts' data. If associated to a "
            "department, gives global access to change all the accounts. If "
            "associated to an account, only gives access to that account."
        ),
    )

    def save(self, *args, **kwargs):
        if self.all_permissions:
            pass
        return models.Model.save(self, *args, **kwargs)
