from captcha.fields import ReCaptchaField
from django import forms

from .models import DepartmentInvitation


class DepartmentInvitationForm(forms.ModelForm):
    email = forms.fields.EmailField(required=True)

    class Meta:
        model = DepartmentInvitation
        fields = ['department', 'account_category', 'email']


class AcceptInvitationForm(forms.Form):
    captcha = ReCaptchaField(attrs={'theme': 'clean'})
