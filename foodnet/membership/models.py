# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)


class FoodnetUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, **kwargs):
        """
        Creates and saves a FoodnetUser with the given username,
        email and password.
        """
        assert username, 'The given username must be set'
        username = self.normalize_email(username)
        user = self.model(username=username, **kwargs)
        for k, v in kwargs.items():
            setattr(user, k, v)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **kwargs):
        user = self.create_user(username, **kwargs)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class FoodnetUser(AbstractBaseUser, PermissionsMixin):
    MALE = 'm'
    FEMALE = 'f'
    SEX_CHOICES = (
        (FEMALE, 'female'),
        (MALE, 'male')
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    username = models.EmailField(unique=True, blank=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    firstname = models.CharField(max_length=255)
    middlename = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)

    # old system: adr1, adr2, streetno, floor, door
    address = models.TextField(max_length=2000)
    postcode = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    tel = models.CharField(max_length=255)
    tel2 = models.CharField(max_length=255)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    dob = models.DateField(null=True)  # old system birthday
    privacy = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    objects = FoodnetUserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        return '{0} {1} {2}'.format(self.firstname, self.middlename,
                                    self.lastname)

    def get_short_name(self):
        return '{0}'.format(self.firstname)

    @property
    def email(self):
        return self.username

    @email.setter
    def email(self, val):
        self.username = val


class Member(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)


class Division(models.Model):
    shortname = models.CharField(max_length=4)
    name = models.CharField(max_length=255)

    # old system: type
    category = models.CharField(max_length=255)

    # old system: webmembers
    allow_webmembers = models.BooleanField()
    contact = models.CharField(max_length=255)

    # FIXME: should we move it out to model manager with
    # other bits from old models?
    # members = models.ManyToManyField('membership.Member',
    #                                 through='membership.DivisionMember')


class DivisionMember(models.Model):
    member = models.ForeignKey(Member)
    division = models.ForeignKey(Division)
    start = models.DateTimeField(auto_now_add=True)
    exit = models.DateTimeField()
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = (('member', 'division'),)
