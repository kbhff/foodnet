from django.contrib import admin

from . import models


@admin.register(models.DepartmentInvitation)
class DepartmentInvitationAdmin(admin.ModelAdmin):
    pass
