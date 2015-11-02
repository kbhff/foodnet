from django.db import models


class Account(models.Model):
    category = models.ForeignKey(
        'accounts.AccountCategory',
        related_name='accounts',
    )

    # TODO: Is an account associated to a department? Or are the departments
    # actually associated to the membership such that economic transactions
    # are NOT coupled to a department!?
    department = models.ForeignKey(
        'departments.Department',
        related_name='accounts',
    )

    # TODO: Accounts do not start and end, we should track memberships that
    # way instead.
    start = models.DateTimeField(auto_now_add=True)
    exit = models.DateTimeField(null=True, default=None, blank=True)

    # TODO: An account cannot be deactivated
    active = models.BooleanField(default=True)

    user_profiles = models.ManyToManyField(
        'profiles.UserProfile',
        related_name='accounts'
    )

    def __str__(self):
        is_active = 'active' if self.active else 'inactive'
        return "{} {} {}".format(self.category, self.department, is_active)


class AccountCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
