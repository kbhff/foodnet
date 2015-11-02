from django.test import TestCase

# Create your tests here.
from eggplant.factories import DepartmentFactory, UserFactory, \
    DepartmentAdministratorFactory, AccountFactory
from eggplant.profiles.models import UserProfile


class TestDeparmentAdmin(TestCase):

    def setUp(self):
        # create dept and admin user
        self.department = DepartmentFactory()
        self.admin_user = UserFactory()
        DepartmentAdministratorFactory(
            profile=self.admin_user.profile, department=self.department)

        # let's add some account/profiles
        self.account1 = AccountFactory(department=self.department)
        self.u1 = UserFactory()

    def test_user_is_department_admin(self):
        profile = self.admin_user.profile
        self.assertTrue(profile.has_admin_permission(self.department),
                        "User does not have admin permission on department")

    def test_admin_can_edit_dept_profiles(self):
        admin = self.admin_user.profile

        profiles = UserProfile.in_department(self.department)

        for profile in profiles:
            self.assertTrue(profile.can_be_edited_by(admin))

    def test_admin_cannot_edit_other_dept_profiles(self):
        admin = self.admin_user.profile

        other_dept = DepartmentFactory()

        for profile in UserProfile.in_department(other_dept):
            self.assertFalse(profile.can_be_edited_by(admin))
