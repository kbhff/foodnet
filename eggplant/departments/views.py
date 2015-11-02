from django.views.generic import ListView

from eggplant.departments.models import Department
from eggplant.profiles.models import UserProfile
from eggplant.core.views import LoginRequiredMixin


class DepartmentProfiles(LoginRequiredMixin, ListView):
    model = UserProfile
    paginate_by = 25
    template_name = 'eggplant/departments/profiles.html'

    def get_queryset(self):
        department = Department.objects.get(slug=self.kwargs.get('slug'))
        queryset = super().get_queryset()
        return queryset.filter(accounts__department=department)

departments_profiles = DepartmentProfiles.as_view()
