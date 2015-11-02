from django.contrib import admin

from . import models


class AccountMembershipInline(admin.TabularInline):
    model = models.Account.user_profiles.through


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    inlines = [AccountMembershipInline]


@admin.register(models.AccountCategory)
class AccountCategoryAdmin(admin.ModelAdmin):
    pass
