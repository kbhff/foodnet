from django import forms


class LoginForm(forms.Form):
    username = forms.EmailField(label='email')
    password = forms.CharField(widget=forms.PasswordInput)
