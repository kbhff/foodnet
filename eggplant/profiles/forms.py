from django import forms

from allauth.account.forms import SetPasswordForm

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


class NewUserSetPasswordForm(SetPasswordForm):
    def save(self, *args, **kwargs):
        self.user.set_password(self.cleaned_data["password1"])
        self.user.save()
