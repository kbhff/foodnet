from allauth.account.forms import (PasswordField, SetPasswordField,
                                   SetPasswordForm)
from django import forms
from django.contrib.auth import get_user_model
from eggplant.profiles.models import UserProfile


class ProfileForm(forms.Form):
    first_name = forms.CharField(label='First name', required=True,
                                 max_length=30)
    middle_name = forms.CharField(label='Middle name', max_length=30,
                                  required=False)
    last_name = forms.CharField(label='Last name', required=True,
                                max_length=30)
    address = forms.CharField(widget=forms.Textarea, label='Address',
                              required=True, max_length=255)
    city = forms.CharField(label='City', required=True, max_length=50)
    postcode = forms.CharField(label='Post code', required=True, max_length=30)
    tel = forms.CharField(label='Phone', required=True, max_length=15)
    sex = forms.ChoiceField(choices=UserProfile.SEX_CHOICES, required=False)
    photo = forms.ImageField(label='Photo', required=False)


class SignupForm(ProfileForm):
    email = forms.EmailField(required=True)
    password1 = SetPasswordField(label="Password", required=True)
    password2 = PasswordField(label="Password (again)", required=True)

    def clean_email(self):
        """
        Check if user is already registered and if so raise validation error.

        It may be considered a security hole to inform if a user
        is registered or not but it improves usability.
        """
        email = self.cleaned_data['email']
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email


class NewUserSetPasswordForm(SetPasswordForm):
    def save(self, *args, **kwargs):
        self.user.set_password(self.cleaned_data["password1"])
        self.user.save()
