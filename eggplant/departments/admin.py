from django.contrib import admin

from .models import Department, DepartmentAdministrator


class DepartmentAdministratorInline(admin.TabularInline):
    model = DepartmentAdministrator


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    inlines = [DepartmentAdministratorInline]
