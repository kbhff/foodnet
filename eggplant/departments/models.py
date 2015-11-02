from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


class Department(models.Model):
    name = models.CharField(
        verbose_name=_("department name"),
        max_length=255,
        blank=False,
    )
    slug = models.SlugField()

    site = models.ForeignKey(
        'sites.Site',
        default=settings.SITE_ID
    )

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        super().save(**kwargs)


class DepartmentAdministrator(models.Model):
    department = models.ForeignKey('departments.Department')
    profile = models.ForeignKey('profiles.UserProfile',
                                related_name='administrator_for')
    created = models.DateTimeField(auto_now_add=True)
