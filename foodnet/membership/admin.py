from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import User, UserProfile, Department, DepartmentMembership,\
    Invitation, Member, MemberCategory, DepartmentCategory, DepartmentAdministrator


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    exclude = ['member', ]


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )


class DepartmentMembershipInline(admin.TabularInline):
    model = DepartmentMembership
    extra = 1


class MemberAdmin(admin.ModelAdmin):
    inlines = (DepartmentMembershipInline,)


class DepartmentAdmin(admin.ModelAdmin):
    inlines = (DepartmentMembershipInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(DepartmentCategory)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(DepartmentMembership)
admin.site.register(DepartmentAdministrator)
admin.site.register(Invitation)
admin.site.register(Member, MemberAdmin)
admin.site.register(MemberCategory)
