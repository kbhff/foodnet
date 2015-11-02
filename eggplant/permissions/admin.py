from django.contrib import admin

from .models import Permission, UserProfilePermission


admin.register(Permission)
admin.register(UserProfilePermission)
